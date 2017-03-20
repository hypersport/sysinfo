# coding=utf-8
from . import main
from flask import render_template
import os
import psutil
import datetime
import netifaces


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
    users = psutil.users()

    return render_template('index.html',
                           sys_name=info[1],
                           kernel_name=info[0],
                           kernel_no=info[2],
                           kernel_version=info[3],
                           sys_framework=info[4],
                           now_time=now_time_format,
                           boot_time=boot_time_format,
                           up_time=up_time,
                           users=users
                           )


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


@main.route('/memory')
def memory():
    memory_info = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()

    return render_template('memory.html', memory_info=memory_info, swap_memory=swap_memory)


@main.route('/disks')
def disks():
    physical_disks_info = []
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
        physical_disks_info.append(physical_disk)

    disks_info = []
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
        disks_info.append(disk)

    disks_io_info = psutil.disk_io_counters(perdisk=True)

    return render_template('disks.html',
                           physical_disks_info=physical_disks_info,
                           disks_info=disks_info,
                           disks_io_info=disks_io_info
                           )


@main.route('/network')
def network():
    net_io_counts = psutil.net_io_counters(pernic=True)
    interfaces_io = []
    for interface in net_io_counts:
        interface_dict = {}
        addrs = netifaces.ifaddresses(interface)
        ipv4_addr_info = addrs.get(2, None)
        ipv4_addr = None
        if ipv4_addr_info:
            ipv4_addr = ipv4_addr_info[0].get('addr', None)
        ipv6_addr_info = addrs.get(10, None)
        ipv6_addr = None
        if ipv6_addr_info:
            ipv6_addr = ipv6_addr_info[0].get('addr', None)
        interface_dict[interface] = [
            addrs[17][0]['addr'],  # MAC address
            ipv4_addr,  # IPV4 address
            ipv6_addr,  # IPV6 address
            net_io_counts[interface].bytes_sent,
            net_io_counts[interface].bytes_recv,
            net_io_counts[interface].packets_sent,
            net_io_counts[interface].packets_recv,
            net_io_counts[interface].errin,
            net_io_counts[interface].errout,
            net_io_counts[interface].dropin,
            net_io_counts[interface].dropout
        ]
        interfaces_io.append(interface_dict)

        net_connections = psutil.net_connections('all')

    return render_template('network.html', interfaces_io=interfaces_io, net_connections=net_connections)
