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
from home_application.models import HostInfo,CeleryHostInfo,CeleryVMsLatestInfo,DatastoreInfo
from vmware import reset_config,set_vm_datastore
from models import DebugInfo

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

def datastore_info(request):
    """
    主机列表
    """
    datastore_datas = DatastoreInfo.objects.all().order_by("dt_volumes")
    return render_mako_context(request, '/home_application/datastore_info.html',{ "datastore_datas": datastore_datas})

def host_info(request):
    """
    主机列表
    """
    host_datas = CeleryHostInfo.objects.all()
    return render_mako_context(request, '/home_application/host_info.html',{"host_datas": host_datas})

def vms_info(request):
    """
    虚机列表
    """
    vms_datas = CeleryVMsLatestInfo.objects.all()
    return render_mako_context(request, '/home_application/vms_info.html',{ "vms_datas": vms_datas})

def portrait_scaling(request):
    """
    纵向扩缩
    """
    return render_mako_context(request, '/home_application/portrait_scaling.html')

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

def reset_vms_cpu(request):
    reset_hostip = request.POST.get('resetcpu_hostip', '')
    reset_vmnum = request.POST.get('resetcpu_vmnum', '')
    reset_cpu = int(request.POST.get('resetcpu_cpu', ''))
    #print type(reset_cpu)
    #print reset_hostip,reset_vmip,reset_cpu
    host_name_value = HostInfo.objects.filter(host_ip=reset_hostip).values('host_name')[0].values()[0]
    host_password_value = HostInfo.objects.filter(host_ip=reset_hostip).values('host_password')[0].values()[0]
    vm_name_value = CeleryVMsLatestInfo.objects.filter(vm_number=reset_vmnum).values('vm_name')[0].values()[0]
    vm_status = CeleryVMsLatestInfo.objects.filter(vm_number=reset_vmnum).values('vm_status')[0].values()[0]
    #print reset_hostip, reset_vmnum, reset_cpu, host_name_value, host_password_value, vm_name_value
    if vm_status == "gray":
        res = reset_config(host_ip=reset_hostip, host_name=host_name_value, host_password=host_password_value, vm_type='cpu',
                     vm_name=vm_name_value, vm_reset=reset_cpu)
        if res:
            return render_json({'result': 1})
        else:
            return render_json({'result': 2})
    else:
        return render_json({'result': 3})

def reset_vms_mem(request):
    reset_hostip = request.POST.get('resetmem_hostip', '')
    reset_vmnum = request.POST.get('resetmem_vmnum', '')
    reset_mem = int(request.POST.get('resetmem_mem', ''))
    # print type(reset_cpu)
    #print reset_hostip,reset_vmnum,reset_mem
    host_name_value = HostInfo.objects.filter(host_ip=reset_hostip).values('host_name')[0].values()[0]
    host_password_value = HostInfo.objects.filter(host_ip=reset_hostip).values('host_password')[0].values()[0]
    vm_name_value = CeleryVMsLatestInfo.objects.filter(vm_number=reset_vmnum).values('vm_name')[0].values()[0]
    vm_status = CeleryVMsLatestInfo.objects.filter(vm_number=reset_vmnum).values('vm_status')[0].values()[0]
    if vm_status == "gray":
        res = reset_config(host_ip=reset_hostip, host_name=host_name_value, host_password=host_password_value,
                           vm_type='memory',vm_name=vm_name_value, vm_reset=reset_mem)
        if res:
            return render_json({'result': 1})
        else:
            return render_json({'result': 2})
    else:
        return render_json({'result': 3})

def reset_vms_data(request):
    reset_hostip = request.POST.get('resetdata_hostip', '')
    reset_vmnum = request.POST.get('resetdata_vmnum', '')
    reset_data = int(request.POST.get('resetdata', ''))
    DebugInfo.objects.create(text_info=reset_hostip + reset_vmnum + reset_data)
    host_name_value = HostInfo.objects.filter(host_ip=reset_hostip).values('host_name')[0].values()[0]
    host_password_value = HostInfo.objects.filter(host_ip=reset_hostip).values('host_password')[0].values()[0]
    vm_name_value = CeleryVMsLatestInfo.objects.filter(vm_number=reset_vmnum).values('vm_name')[0].values()[0]
    vm_status = CeleryVMsLatestInfo.objects.filter(vm_number=reset_vmnum).values('vm_status')[0].values()[0]
    #print host_name_value,host_password_value,vm_name_value,vm_status
    DebugInfo.objects.create(text_info=host_name_value + host_password_value + vm_name_value + vm_status)
    if vm_status == "gray":
        res = set_vm_datastore(host_ip=reset_hostip, host_name=host_name_value, host_password=host_password_value,
                           vm_name=vm_name_value, reservation=reset_data)
        if res:
            return render_json({'result': 1})
        else:
            return render_json({'result': 2})
    else:
        return render_json({'result': 3})