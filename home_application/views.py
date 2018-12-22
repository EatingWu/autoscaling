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

from common.mymako import render_mako_context,render_json
from home_application.models import HostInfo


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')

def host_list(request):
    """
    主机列表
    """
    datas = HostInfo.objects.all()
    return render_mako_context(request, '/home_application/host_list.html',{ "datas": datas})

def record_host(request):
    '''
    录入主机
    :param request:
    :return:
    '''
    host_ip = request.POST.get('host_ip', '')
    host_name = request.POST.get('host_name', '')
    host_password = request.POST.get('host_password', '')
    if host_ip:
        check_ip = HostInfo.objects.filter(host_ip=host_ip).values("host_ip")
        if check_ip:
            return render_json({'result': 1})
        else:
            data = HostInfo(host_ip=host_ip, host_name=host_name, host_password=host_password)
            data.save()
            return render_json({'result': 2})
    else:
        return render_json({'result': 3})