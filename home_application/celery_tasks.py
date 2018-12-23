# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from models import HostInfo,CeleryHostInfo
from vmware import  get_host_info

from common.log import logger


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))

@task()
def check_host_status():
    hosts_dict_flag = False
    hosts_dict_datalist = []
    host_info_len = HostInfo.objects.count()
    for host_info_id in range(1, host_info_len + 1):
        #print host_info_id
        ip_value = HostInfo.objects.filter(id=host_info_id).values('host_ip')[0].get('host_ip')
        name_value = HostInfo.objects.filter(id=host_info_id).values('host_name')[0].get('host_name')
        password_value = HostInfo.objects.filter(id=host_info_id).values('host_password')[0].get('host_password')
        #print ip_value, name_value, password_value
        hosts_dict_datalist = get_host_info(ip_value, name_value, password_value)
        #print dir(CeleryHostInfo.objects)
        hosts_dict_data_len = len(hosts_dict_datalist)
        for host_info in range(0,hosts_dict_data_len):
            #print(hosts_dict_datalist[host_info].get("hostname"))
            host_name = CeleryHostInfo.objects.filter(host_name=hosts_dict_datalist[host_info].get("hostname")).values("host_name")
            if host_name:
                #print "exist"
                CeleryHostInfo.objects.filter(host_name=hosts_dict_datalist[host_info].get('hostname')).update(host_ip=ip_value,
                                              cpu_usage=hosts_dict_datalist[host_info].get('hostcpuusagepercent'),
                                              mem_usage=hosts_dict_datalist[host_info].get('hostmemoryusagepercent'),
                                              running_vms=hosts_dict_datalist[host_info].get('hostrunningvms'),
                                              stopped_vms=hosts_dict_datalist[host_info].get('hoststoppedvms'),
                                              total_vms=hosts_dict_datalist[host_info].get('hosttotalvms'),
                                              status=hosts_dict_datalist[host_info].get('hoststatus'))
            else:
                #print "new"
                CeleryHostInfo.objects.create(host_ip=ip_value, host_name=hosts_dict_datalist[host_info].get('hostname'),
                                              cpu_usage=hosts_dict_datalist[host_info].get('hostcpuusagepercent'),
                                              mem_usage=hosts_dict_datalist[host_info].get('hostmemoryusagepercent'),
                                              running_vms=hosts_dict_datalist[host_info].get('hostrunningvms'),
                                              stopped_vms=hosts_dict_datalist[host_info].get('hoststoppedvms'),
                                              total_vms=hosts_dict_datalist[host_info].get('hosttotalvms'),
                                              status=hosts_dict_datalist[host_info].get('hoststatus'))


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    check_host_status.apply_async()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))
