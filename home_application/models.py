# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from django.db import models

'''
主机列表
'''
class HostInfo(models.Model):
    host_ip = models.CharField(max_length=32)
    host_name = models.CharField(max_length=50)
    host_password = models.CharField(max_length=50)

    class Meta:
        verbose_name = u"主机IP"
        verbose_name_plural = u"主机IP"

'''
主机状态
'''
class CeleryHostInfo(models.Model):
    host_ip = models.CharField(max_length=32)
    host_name = models.CharField(max_length=32)
    cpu_usage = models.FloatField(max_length=32)
    mem_usage = models.FloatField(max_length=32)
    running_vms = models.IntegerField()
    stopped_vms = models.IntegerField()
    total_vms = models.IntegerField()
    status = models.CharField(max_length=32)

    class Meta:
        verbose_name = u"主机状态"
        verbose_name_plural = u"主机状态"