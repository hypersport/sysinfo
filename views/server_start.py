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
    user_percent = cpu_time_percent[0]
    sys_percent = cpu_time_percent[2]
    idle_percent = cpu_time_percent[3]
    iowait_percent = cpu_time_percent[4]
    nice_percent = cpu_time_percent[1]
    else_percent = 0.0
    for i in range(5, 10):
        else_percent += cpu_time_percent[i]
    run_freq = round(psutil.cpu_freq()[0] / 1000, 1)
    min_freq = round(psutil.cpu_freq()[1] / 1000, 1)
    max_freq = round(psutil.cpu_freq()[2] / 1000, 1)

    return render_template('cpu.html',
                           physical_core_num=physical_core_num,
                           logical_core_num=logical_core_num,
                           load_avg=load_avg,
                           user_percent=user_percent,
                           sys_percent=sys_percent,
                           idle_percent=idle_percent,
                           iowait_percent=iowait_percent,
                           nice_percent=nice_percent,
                           else_percent=nice_percent,
                           run_freq=run_freq,
                           min_freq=min_freq,
                           max_freq=max_freq
                           )
