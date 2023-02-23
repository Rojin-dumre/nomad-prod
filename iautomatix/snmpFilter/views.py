from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SnmpSerializer

import os

from pysnmp.hlapi import *

from puresnmp import walk



from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result, print_title
from nornir_utils.plugins.tasks.files import write_file
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.task import Result, Task
from nornir.core.filter import F

from .models import Snmp 

@api_view(['GET'])
def snmpList(request):
    snmps = Snmp.objects.all()
    serializer = SnmpSerializer(snmps, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def snmpDetail(request, pk):
    snmps = Snmp.objects.get(id=pk)
    serializer = SnmpSerializer(snmps, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def snmpCreate(request):
    serializer = SnmpSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)


@api_view(['POST'])
def snmpUpdate(request, pk):
    snmp = Snmp.objects.get(id=pk)
    serializer = SnmpSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.saved()

    return Response(serializer.data)


@api_view(['DELETE'])
def snmpDelete(request, pk):
    snmp = Snmp.objects.get(id=pk)
    snmp.delete()

    return Response('Item successfully deleted!')



@api_view(['GET'])
def snmpTree(request, host):

    path = os.getcwd()
    configYamlPath = path + "/snmpFilter/config.yaml"

    
    # oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.9.1.2.2'))

    # g = getCmd(
    #     SnmpEngine(), CommunityData('public'), UdpTransportTarget(
    #         (m, 161), retries=0), ContextData(), ObjectType(
    #             ObjectIdentity()
    #         )
    # )

    # for(errorIndication, errorStatus, errorIndex, varBinds) in g:
    #     if errorIndication or errorStatus:
    #         print(f"Error: {errorIndication or errorStatus}")
    #     else:
    #         for varBind in varBinds:
    #             print(f"{varBind[0]} = {varBind[1]}")


    IP = "10.1.1.1"
    COMMUNITY = 'public'
    OID = '1.3.6.1.2.1.2'
    
    for row in walk(IP, COMMUNITY, OID):
        print(row)

    return Response('Done')