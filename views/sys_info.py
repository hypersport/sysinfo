# coding=utf-8
from . import main
from flask import render_template
import os
import psutil
import datetime


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

    return render_template('memory.html',
                           memory_info=memory_info,
                           swap_memory=swap_memory
                           )
