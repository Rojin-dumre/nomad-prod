from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SnmpSerializer

import os

from pysnmp.hlapi import *

from puresnmp import walk

import re

import json



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



    # Specify the OID you want to query
    # oid = ObjectIdentifier('1.3.6.1.2.1.1')

    # # Create a SNMP engine instance
    # snmp_engine = SnmpEngine()

    # # Create a SNMP bulk iterator for the OID
    # iterator = bulkCmd(
    #     snmp_engine,
    #     CommunityData('public'),  # Replace with your SNMP community string
    #     UdpTransportTarget(('10.10.10.254', 161)),  # Replace with your SNMP agent's IP address and port
    #     ContextData(),
    #     0,  # Non-repeaters (0 for bulkCmd)
    #     10,  # Max-repetitions (number of sub-IDs to retrieve in each iteration)
    #     ObjectType(ObjectIdentity(oid)),
    #     lexicographicMode=False
    # )
    # general_descriptions = {}

    # # Iterate over the OID and its sub-IDs
    # for i, response in enumerate(iterator):
    #     if i == 9:
    #         break
    #     for var_bind in response[3]:
    #         oid_str = str(var_bind[0])
    #         if not oid.isPrefixOf(ObjectIdentifier(oid_str)):  #checks if the oid represented by the "ObjectIdentifier" instnce "oid" is a prefix of the OID represented by the 'ObjectIdentifier' instance created from the var-bind OID string f the OID is not a prefix, it means that we have moved on to a different OID subtree, so the inner for loop is broken using the break statement.
    #             break
    #         general_descriptions.update({oid_str: var_bind[1].prettyPrint()})

    # print(general_descriptions)

    oid = ObjectIdentifier('1.3.6.1.2.1.2')

  
    snmp_engine = SnmpEngine()

    # Create a SNMP bulk iterator for the OID
    iterator = bulkCmd(
        snmp_engine,
        CommunityData('public'),  # Replace with your SNMP community string
        UdpTransportTarget(('10.10.10.254', 161)),  # Replace with your SNMP agent's IP address and port
        ContextData(),
        0,  # Non-repeaters (0 for bulkCmd)
        10,  # Max-repetitions (number of sub-IDs to retrieve in each iteration)
        ObjectType(ObjectIdentity(oid)),
        lexicographicMode=False
    )
    
    total_interfaces = {}
    interface_index = {}
    interface_description = {}
    interface_type = {}
    interface_largest_datagram = {}
    interface_bandwidth = {}
    interface_physical_address = {}
    interface_desired_state = {}
    interface_operational_state = {}
    interface_last_change = {}
    interface_octets_in = {}
    interface_unicast_packets_in = {}
    interface_nonunicast_packets_in = {}
    interface_inbound_discards = {}
    interface_errors_in = {}
    interface_unknown_protocol_in = {}

    interface_octets_out = {}
    interface_unicast_packets_out = {}
    interface_nonunicast_packets_out = {}
    interface_outbound_discards = {}
    interface_errors_out = {}
    # interface_output_queue_length = {}





    j = 0
    previous_oid_str = ObjectIdentifier('1.1.1.1')

    # Iterate over the OID and its sub-IDs
    for i, response in enumerate(iterator):
        # if i == 50:
        #     break
        # i starts with o
        
        for var_bind in response[3]:
            
            oid_str = str(var_bind[0])

            new_oid_str = re.sub(r'\.\d+$', '', oid_str)

            # print(new_oid_str)
            # print(previous_oid_str)     

            if new_oid_str != previous_oid_str:
                # print("This is a break")   
                j = j +1  

            if j == 1:
                total_interfaces.update({oid_str: var_bind[1].prettyPrint()})

            if j == 2:
                interface_index.update({oid_str: var_bind[1].prettyPrint()})

            if j == 3:
                interface_description.update({oid_str: var_bind[1].prettyPrint()})

            if j == 4:
                interface_type.update({oid_str: var_bind[1].prettyPrint()})
            
            if j == 5:
                interface_largest_datagram.update({oid_str: var_bind[1].prettyPrint()})

            if j == 6:
                interface_bandwidth.update({oid_str: var_bind[1].prettyPrint()})

            if j == 7:
                interface_physical_address.update({oid_str: var_bind[1].prettyPrint()})
            
            if j == 8:
                interface_desired_state.update({oid_str: var_bind[1].prettyPrint()})

            if j == 9:
                interface_operational_state.update({oid_str: var_bind[1].prettyPrint()})

            if j == 10:
                interface_last_change.update({oid_str: var_bind[1].prettyPrint()})
            
            if j == 11:
                interface_octets_in.update({oid_str: var_bind[1].prettyPrint()})
            
            if j == 12:
                interface_unicast_packets_in.update({oid_str: var_bind[1].prettyPrint()})
            
            if j == 13:
                interface_inbound_discards.update({oid_str: var_bind[1].prettyPrint()})

                       



            

            

            if not oid.isPrefixOf(ObjectIdentifier(oid_str)):  #checks if the oid represented by the "ObjectIdentifier" instnce "oid" is a prefix of the OID represented by the 'ObjectIdentifier' instance created from the var-bind OID string f the OID is not a prefix, it means that we have moved on to a different OID subtree, so the inner for loop is broken using the break statement.
                break

            previous_oid_str = re.sub(r'\.\d+$', '', oid_str)
            
            
    

    response_data = {
        'interface_total': json.dumps(list(total_interfaces.values())),
        'interface_description': json.dumps(list(interface_description.values())),
        'interface_type': json.dumps(list(interface_type.values())),
        'interface_largest_datagram': json.dumps(list(interface_largest_datagram.values())),
        'interface_bandwidth': json.dumps(list(interface_bandwidth.values())),
        'interface_physical_address': json.dumps(list(interface_physical_address.values())),
        'interface_desired_state': json.dumps(list(interface_desired_state.values())),
        'interface_operational_state': json.dumps(list(interface_operational_state.values())),
        'interface_last_change': json.dumps(list(interface_last_change.values())),
        'interface_octets_in': json.dumps(list(interface_octets_in.values())),
        'interface_unicast_packets_in': json.dumps(list(interface_unicast_packets_in.values())),
        'interface_inbound_discards': json_dumps(list(interface_inbound_discards.values()))



    }

    










    # IP = "10.1.1.1"
    # COMMUNITY = 'public'
    # OID = '1.3.6.1.2.1.1.0.2'
    
    # for row in walk(IP, COMMUNITY, OID):
    #     print(row)

    return Response(response_data)

