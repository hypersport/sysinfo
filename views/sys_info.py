# coding=utf-8
from . import main
from flask import render_template
from .tools import get_rlimits
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


@main.route('/cpu')
def cpu_info():
    logical_core_num = psutil.cpu_count()
    physical_core_num = psutil.cpu_count(logical=False)
    load_avg = os.getloadavg()
    cpu_time_percent = psutil.cpu_times_percent()
    else_percent = 0.0
    for i in range(5, 10):
        else_percent += cpu_time_percent[i]
    cpu_freq = psutil.cpu_freq()

    return render_template('cpu.html',
                           physical_core_num=physical_core_num,
                           logical_core_num=logical_core_num,
                           load_avg=load_avg,
                           cpu_time_percent=cpu_time_percent,
                           else_percent=else_percent,
                           cpu_freq=cpu_freq
                           )


@main.route('/memory/', defaults={'part': 'memory'})
@main.route('/memory/<string:part>')
def memory(part):
    if part == 'memory':
        context = psutil.virtual_memory()
    elif part == 'swap':
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
            physical_disk_usage = psutil.disk_usage(physical_disk_partition.mountpoint)
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
        context.sort(key=lambda partition: partition.get(sort), reverse=True if order == 'desc' else False)

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
                net_io_counts[interface].bytes_sent,
                net_io_counts[interface].bytes_recv,
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
        context.sort(key=lambda connect: connect.status if connect.status != 'NONE' else 'z')
    else:
        return render_template('404.html'), 404

    return render_template('network/%s.html' % part, context=context, part=part)


@main.route('/processes', defaults={'sort': 'cpu', 'order': 'desc'})
@main.route('/processes/<string:sort>')
@main.route('/processes/<string:sort>/<string:order>')
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
        processes.sort(key=lambda proc: proc.get(sort), reverse=True if order == 'desc' else False)
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
        process_info['parent'] = parent_process.name() if parent_process else None
        process_info['cpu_affinity'] = [str(n) for n in process_info['cpu_affinity']]
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
