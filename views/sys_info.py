from . import main
from flask import render_template, jsonify
from .tools import get_rlimits, b_to_m
import os
import psutil
import datetime
import netifaces


@main.errorhandler(psutil.NoSuchProcess)
def no_such_process(e):
    return render_template('404.html'), 404


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.route('/')
def index():
    info = os.uname()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    boot_time_format = boot_time.strftime("%Y-%m-%d %H:%M:%S")
    now_time = datetime.datetime.now()
    now_time_format = now_time.strftime("%Y-%m-%d %H:%M:%S")
    up_time = "{} 天 {} 小时 {} 分钟 {} 秒".format(
        (now_time - boot_time).days,
        str(now_time - boot_time).split('.')[0].split(':')[0],
        str(now_time - boot_time).split('.')[0].split(':')[1],
        str(now_time - boot_time).split('.')[0].split(':')[2]
    )

    return render_template('index.html',
                           sys_name=info[1],
                           kernel_name=info[0],
                           kernel_no=info[2],
                           kernel_version=info[3],
                           sys_framework=info[4],
                           now_time=now_time_format,
                           boot_time=boot_time_format,
                           up_time=up_time
                           )


@main.route('/users')
def all_user():
    users = psutil.users()

    return render_template('users.html', users=users)


@main.route('/cpu', defaults={'chart': None})
@main.route('/cpu/<string:chart>')
def cpu_info(chart):
    if chart in ['line', 'pie']:
        return render_template('cpu/cpu-%s.html' % chart, chart=chart)
    logical_core_num = psutil.cpu_count()
    physical_core_num = psutil.cpu_count(logical=False)
    load_avg = os.getloadavg()
    cpu_time_percent = psutil.cpu_times_percent()
    else_percent = 0.0
    for i in range(5, 10):
        else_percent += cpu_time_percent[i]
    try:
        cpu_freq = psutil.cpu_freq()
    except AttributeError:
        cpu_freq = None

    return render_template('cpu/cpu_info.html',
                           physical_core_num=physical_core_num,
                           logical_core_num=logical_core_num,
                           load_avg=load_avg,
                           cpu_time_percent=cpu_time_percent,
                           else_percent=else_percent,
                           cpu_freq=cpu_freq,
                           )


@main.route('/memory/', defaults={'part': 'memory', 'chart': None})
@main.route('/memory/<string:part>')
@main.route('/memory/<string:part>/<string:chart>')
def memory(part, chart=None):
    if part == 'memory':
        if chart in ['line', 'column']:
            return render_template('memory/memory-%s.html' % chart, part=part, chart=chart)
        context = psutil.virtual_memory()
    elif not chart and part == 'swap':
        context = psutil.swap_memory()
    else:
        return render_template('404.html'), 404

    return render_template('memory/%s.html' % part, context=context, part=part)


@main.route('/disks/', defaults={'part': 'disk', 'sort': 'space_free', 'order': 'desc'})
@main.route('/disks/<string:part>')
@main.route('/disks/<string:part>/<string:sort>')
@main.route('/disks/<string:part>/<string:sort>/<string:order>')
def disks(part='disk', sort='space_free', order='desc'):
    if part == 'disk':
        context = []
        physical_disk_partitions = psutil.disk_partitions()
        for physical_disk_partition in physical_disk_partitions:
            physical_disk_usage = psutil.disk_usage(
                physical_disk_partition.mountpoint)
            physical_disk = {
                'device': physical_disk_partition.device,
                'mount_point': physical_disk_partition.mountpoint,
                'type': physical_disk_partition.fstype,
                'options': physical_disk_partition.opts,
                'space_total': physical_disk_usage.total,
                'space_used': physical_disk_usage.used,
                'used_percent': physical_disk_usage.percent,
                'space_free': physical_disk_usage.free
            }
            context.append(physical_disk)

    elif part == 'partition':
        context = []
        disk_partitions_all = psutil.disk_partitions(all=True)
        for disk_partition in disk_partitions_all:
            disk_usage = psutil.disk_usage(disk_partition.mountpoint)
            disk = {
                'device': disk_partition.device,
                'mount_point': disk_partition.mountpoint,
                'type': disk_partition.fstype,
                'options': disk_partition.opts,
                'space_total': disk_usage.total,
                'space_used': disk_usage.used,
                'used_percent': disk_usage.percent,
                'space_free': disk_usage.free
            }
            context.append(disk)
        context.sort(key=lambda partition: partition.get(sort),
                     reverse=True if order == 'desc' else False)

    elif part == 'io':
        context = psutil.disk_io_counters(perdisk=True)
    else:
        return render_template('404.html'), 404

    return render_template('disks/%s.html' % part, context=context, part=part, sort=sort, order=order)


@main.route('/network/', defaults={'part': 'interfaces'})
@main.route('/network/<string:part>')
def network(part):
    if part == 'interfaces':
        net_io_counts = psutil.net_io_counters(pernic=True)
        context = []
        for interface in net_io_counts:
            interface_dict = {}
            addrs = netifaces.ifaddresses(interface)
            ipv4_addr_info = addrs.get(2, None)
            ipv4_addr = ''
            if ipv4_addr_info:
                ipv4_addr = ipv4_addr_info[0].get('addr', '')
            ipv6_addr_info = addrs.get(10, None)
            ipv6_addr = ''
            if ipv6_addr_info:
                ipv6_addr = ipv6_addr_info[0].get('addr', '').split('%')[0]
            interface_dict[interface] = [
                addrs[17][0]['addr'],  # MAC address
                ipv4_addr,
                ipv6_addr,
                b_to_m(net_io_counts[interface].bytes_sent),
                b_to_m(net_io_counts[interface].bytes_recv),
                net_io_counts[interface].packets_sent,
                net_io_counts[interface].packets_recv,
                net_io_counts[interface].errin,
                net_io_counts[interface].errout,
                net_io_counts[interface].dropin,
                net_io_counts[interface].dropout
            ]
            context.append(interface_dict)
    elif part == 'connections':
        context = psutil.net_connections(kind='all')
        context.sort(
            key=lambda connect: connect.status if connect.status != 'NONE' else 'z')
    elif part == 'traffic':
        return render_template('network/traffic-statistics.html', part=part)
    else:
        return render_template('404.html'), 404

    return render_template('network/%s.html' % part, context=context, part=part)


@main.route('/processes', defaults={'sort': 'cpu', 'order': 'desc'})
@main.route('/processes/<string:sort>')
@main.route('/processes/<string:sort>/<string:order>')
@main.before_app_first_request
def all_process(sort='cpu', order='asc'):
    processes = []
    for p in psutil.process_iter():
        process_info = {
            'name': p.name(),
            'pid': p.pid,
            'username': p.username(),
            'cpu': p.cpu_percent(),
            'memory': p.memory_percent(),
            'memory_rss': p.memory_info().rss,
            'memory_vms': p.memory_info().vms,
            'status': p.status(),
            'created_time': p.create_time(),
            'cmdline': ' '.join(p.cmdline())
        }
        processes.append(process_info)
        processes.sort(key=lambda proc: proc.get(sort),
                       reverse=True if order == 'desc' else False)
    return render_template('processes.html', processes=processes, sort=sort, order=order)


@main.route('/process/<int:pid>/', defaults={'part': 'process'})
@main.route('/process/<int:pid>/<string:part>')
def process(pid, part):
    the_process = psutil.Process(pid)
    process_info = {}
    parts = ['process', 'memory', 'threads', 'files', 'connections', 'environ']
    if part in parts:
        parent_process = the_process.parent()
        process_info = the_process.as_dict()
        process_info['parent'] = parent_process.name(
        ) if parent_process else None
        process_info['cpu_affinity'] = [
            str(n) for n in process_info['cpu_affinity']]
    elif part == 'limits':
        process_info['limits'] = get_rlimits(the_process)
    elif part == 'children':
        children = []
        for p in the_process.children():
            child = {
                'pid': p.pid,
                'name': p.name(),
                'username': p.username(),
                'status': p.status()
            }
            children.append(child)
        process_info['children'] = children
    else:
        return render_template('404.html'), 404

    return render_template('process/%s.html' % part, process_info=process_info, pid=pid, part=part)


@main.route('/api', defaults={'part': 'cpu', 'chart': 'line'})
@main.route('/api/<string:part>/')
@main.route('/api/<string:part>/<string:chart>')
def api(part, chart):
    if part == 'cpu':
        cpu_info = {}
        cpu_time_percent = psutil.cpu_times_percent()
        if chart == 'line':
            cpu_info = {'used_cpu_percent': cpu_time_percent.user +
                        cpu_time_percent.system}
        elif chart == 'pie':
            else_percent = 0.0
            for i in range(5, 10):
                else_percent += cpu_time_percent[i]
            cpu_info = {
                'used_by_user': cpu_time_percent.user,
                'used_by_system': cpu_time_percent.system,
                'free': cpu_time_percent.idle,
                'else_percent': else_percent
            }
        return cpu_info

    elif part == 'memory':
        memory_info = {}
        context = psutil.virtual_memory()
        if chart == 'line':
            memory_info = {'used_mem_percent': context.percent}
        elif chart == 'column':
            memory_info = {
                'total': b_to_m(context.total),
                'available': b_to_m(context.available),
                'used': b_to_m(context.used),
                'free': b_to_m(context.free),
                'buffers': b_to_m(context.buffers),
                'cached': b_to_m(context.cached),
                'shared': b_to_m(context.shared),
            }
        return memory_info

    elif part == 'traffic':
        net_io_counts = psutil.net_io_counters(pernic=True)
        traffic_statistics = []
        for interface in net_io_counts:
            interface_dict = {}
            interface_dict[interface] = [
                b_to_m(net_io_counts[interface].bytes_sent),
                b_to_m(net_io_counts[interface].bytes_recv),
                net_io_counts[interface].packets_sent,
                net_io_counts[interface].packets_recv
            ]
            traffic_statistics.append(interface_dict)
        return jsonify(traffic_statistics)
