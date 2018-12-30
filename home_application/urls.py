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

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^host_list/$', 'host_list'),
    (r'^host_info/$', 'host_info'),
    (r'^datastore_info/$', 'datastore_info'),
    (r'^vms_info/$', 'vms_info'),
    (r'^portrait_scaling/$', 'portrait_scaling'),
    (r'^record_host/$', 'record_host'),
    (r'^reset_vms_cpu/$', 'reset_vms_cpu'),
    (r'^reset_vms_mem/$', 'reset_vms_mem'),
    (r'^reset_vms_data/$', 'reset_vms_data'),
)
