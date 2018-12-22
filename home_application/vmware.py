# -*- coding: utf-8 -*-

from __future__ import division
import pysphere
from pysphere import VIServer, MORTypes, VIProperty, VIMor, VITask
from pysphere.vi_virtual_machine import VIVirtualMachine
from pysphere.resources import VimService_services as VI
import pprint
import ssl
ssl._create_default_https_context = ssl._create_unverified_context #解决python出现ssl：certificate_verify_failed

'''
输出主机信息
'''
def get_host_info(host_ip,host_name,host_password):
    hosts_dict_data = [
        {'hostbiosinfo': '-[FHE108SUS-1.30]-',
         'hostcpuhealthinfo': 'green',
         'hostcputotal': 31920,
         'hostcpuusage': 1879,
         'hostcpuusagepercent': 5.89,
         'hostmemoryusage': 55819,
         'hostmemoryusagepercent': 42.6,
         'hostname': '172.51.193.21',
         'hostrunningvms': 11,
         'hoststatus': 0,
         'hoststoppedvms': 3,
         'hosttotalmemory': 131042.0390625,
         'hosttotalvms': 14,
         'hosttype': 'IBM NeXtScale nx360 M4: -[5455I7A]-'},
        {'hostbiosinfo': '-[FHE108SUS-1.30]-',
         'hostcpuhealthinfo': 'green',
         'hostcputotal': 31920,
         'hostcpuusage': 408,
         'hostcpuusagepercent': 1.28,
         'hostmemoryusage': 29375,
         'hostmemoryusagepercent': 22.42,
         'hostname': '172.51.193.20',
         'hostrunningvms': 15,
         'hoststatus': 0,
         'hoststoppedvms': 7,
         'hosttotalmemory': 131042.0390625,
         'hosttotalvms': 22,
         'hosttype': 'IBM NeXtScale nx360 M4: -[5455I7A]-'},
        {'hostbiosinfo': '3.31',
         'hostcpuhealthinfo': 'green',
         'hostcputotal': 38304,
         'hostcpuusage': 17992,
         'hostcpuusagepercent': 46.97,
         'hostmemoryusage': 15212,
         'hostmemoryusagepercent': 5.81,
         'hostname': '172.51.193.23',
         'hostrunningvms': 1,
         'hoststatus': 0,
         'hoststoppedvms': 1,
         'hosttotalmemory': 261741.41796875,
         'hosttotalvms': 2,
         'hosttype': 'XH628 V3'},
        {'hostbiosinfo': '3.35',
         'hostcpuhealthinfo': 'green',
         'hostcputotal': 38304,
         'hostcpuusage': 1285,
         'hostcpuusagepercent': 3.35,
         'hostmemoryusage': 10215,
         'hostmemoryusagepercent': 3.9,
         'hostname': '172.51.193.22',
         'hostrunningvms': 1,
         'hoststatus': 2,
         'hoststoppedvms': 1,
         'hosttotalmemory': 261741.41796875,
         'hosttotalvms': 2,
         'hosttype': 'XH628 V3'}
    ]
    return hosts_dict_data

def get_host_info2(host_ip,host_name,host_password):
    hosts_dict_data = []
    server = VIServer()
    server.connect(host_ip, host_name, host_password)
    print 'VC connect successful...'

    for d, hname in server.get_hosts().items():

        HostMemoryUsage = 0
        HostCpuUsage = 0
        HostTotalMemory = 0
        HostNumCpuCores = 0
        HostMhzPerCore = 0
        HostStatus = ''

        props = server._retrieve_properties_traversal(property_names=[
            'name',
            'summary.overallStatus',
            'summary.quickStats.overallMemoryUsage',
            'summary.quickStats.overallCpuUsage',
            'summary.hardware.memorySize',
            'summary.hardware.numCpuCores',
            'summary.hardware.cpuMhz',
            'hardware.biosInfo',
            'hardware.systemInfo',
            'summary.runtime.healthSystemRuntime.hardwareStatusInfo.cpuStatusInfo',
            'summary.runtime.healthSystemRuntime.hardwareStatusInfo.memoryStatusInfo',
            'summary.runtime.healthSystemRuntime.hardwareStatusInfo.storageStatusInfo'
        ], from_node=d, obj_type="HostSystem")

        for prop_set in props:
            # mor = prop_set.Obj #in case you need it
            for prop in prop_set.PropSet:
                if prop.Name == "summary.quickStats.overallMemoryUsage":
                    HostMemoryUsage = prop.Val
                elif prop.Name == "summary.quickStats.overallCpuUsage":
                    HostCpuUsage = prop.Val
                elif prop.Name == "summary.hardware.memorySize":
                    HostTotalMemory = (prop.Val / 1048576)
                elif prop.Name == "summary.hardware.numCpuCores":
                    HostNumCpuCores = prop.Val
                elif prop.Name == "summary.hardware.cpuMhz":
                    HostMhzPerCore = prop.Val
                elif prop.Name == "summary.overallStatus":
                    HostStatus = prop.Val
                    if HostStatus == "green":
                        HostStatus = 0
                    elif HostStatus == "gray":
                        HostStatus = 1
                    elif HostStatus == "yellow":
                        HostStatus = 2
                    elif HostStatus == "red":
                        HostStatus = 3
                elif prop.Name == "hardware.biosInfo":
                    HostBiosInfo = prop.Val.__dict__['_biosVersion']
                # print HostBiosInfo
                elif prop.Name == "hardware.systemInfo":
                    HostSystemInfo = prop.Val.__dict__
                    HostType = HostSystemInfo['_model']
                elif prop.Name == "summary.runtime.healthSystemRuntime.hardwareStatusInfo.cpuStatusInfo":
                    HostHealthInfo_cpu = prop.Val.__dict__
                    for i in HostHealthInfo_cpu['_HostHardwareElementInfo']:
                        cpu = i.__dict__
                        cpu1 = cpu['_status'].__dict__
                        HostCPUHealthInfo = cpu1['_label']
                elif prop.Name == "summary.runtime.healthSystemRuntime.hardwareStatusInfo.memoryStatusInfo":
                    HostHealthInfo_memory = prop.Val.__dict__
                    for i in HostHealthInfo_memory['_HostHardwareElementInfo']:
                        mem = i.__dict__
                        mem1 = mem['_status'].__dict__
                        # print mem1
                        HostMemHealthInfo = mem1['_label']
                        # print HostMemHealthInfo
                elif prop.Name == "summary.runtime.healthSystemRuntime.hardwareStatusInfo.storageStatusInfo":
                    HostHealthInfo_storage = prop.Val.__dict__

        HostRunningVMS = len(server.get_registered_vms(d, status='poweredOn'))
        HostStoppedVMS = len(server.get_registered_vms(d, status='poweredOff'))
        HostTotalVMS = len(server.get_registered_vms(d))
        HostCpuTotal = (HostNumCpuCores * HostMhzPerCore)
        HostMemoryUsagePercent = round((HostMemoryUsage * 100) / HostTotalMemory,2)
        HostCpuUsagePercent = round(((HostCpuUsage * 100) / HostCpuTotal),2)

        hosts_dict = {'hostname': hname.lower(), 'hoststatus': HostStatus, 'hostmemoryusage': HostMemoryUsage,
                      'hostcpuusage': HostCpuUsage, 'hosttotalmemory': HostTotalMemory, 'hostcputotal': HostCpuTotal,
                      'hostmemoryusagepercent': HostMemoryUsagePercent, 'hostcpuusagepercent': HostCpuUsagePercent,
                      'hostrunningvms': HostRunningVMS, 'hoststoppedvms': HostStoppedVMS, 'hosttotalvms': HostTotalVMS,
                      'hostbiosinfo': HostBiosInfo, 'hosttype': HostType, 'hostcpuhealthinfo': HostCPUHealthInfo}
        hosts_dict_data.append(hosts_dict)

    server.disconnect()
    return hosts_dict_data