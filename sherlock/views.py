from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers

from sherlock.models import Packet
from platform import system

import socket
import nmap
from .osdata import get_op_sys, get_ip, map_net, scan_network

from json import dumps

# Views
def index(request):
	return render(request, 'homepage/index.html')

def node_map(request):
    return render(request, 'homepage/node-map.html', {})

def host_node(request):
    return render(request, 'host-node/host-node.html', {})

def detail(request, id):
    """This is an example end point which takes an "id" and returns it.

    Args:
        request (Object): request object
        object (int): object id

    Returns:
        HttpResponse: an HTTP response of the id in the request
    """
    return HttpResponse("You're looking at object %s." % id)

def net_traf(request):
    return render(request, 'homepage/network-traffic.html', {})

def network_traffic(request, port):
    """Gets network traffic from a port and returns its data
    
    Args:
        request (Object): [description]

    Returns:
        HttpResponse: an HTTP response of packet data for the request
    """
    return render(request, 'examples/websockets/index.html')


def network_operating_systems(request):
    return HttpResponse('The operating systems on this network are: %s' % (get_op_sys(map_net())))

def host_scan_all(request, ipaddress):
	""" Scan an ipaddress for other hosts """

	nm = nmap.PortScanner()

	scan_info = nm.scan(ipaddress)

	return scan_info['scan'] 

def host_scan(request, ipaddress, portrange):
	""" Scan an ipaddress for other hosts """

	nm = nmap.PortScanner()

	scan_info = nm.scan(ipaddress, portrange)

	return HttpResponse("Other hosts found: %s" % (scan_info['scan']))


def local_ports(request):
    """Scan all local ports 

    Args: 
       request (Object): [description]
    Returns:
      comma separated list in HttpResponse
    """
    open_ports = []

    for port in range(0,65535):
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = test_socket.connect_ex(("127.0.0.1", port))

        if result == 0:
            open_ports.append(port)
        test_socket.close()

    # return HttpResponse(",".join(str(i) for i in open_ports))
    return open_ports

def web_sockets_example(request):
    """Provides a sample websocket connection

    Args:
        request (request): renders a simple web socket application

    Returns:
        HTML
    """
    return render(request, 'examples/websockets/index.html')

def localpage(request):
    
    ports = local_ports(request)
    ports = dumps(ports)
    my_ip = get_ip() 
    other_ips = map_net()
    other_hosts = []

    for other_ip in other_ips:
        if my_ip == other_ip:
            other_ips.remove(other_ip)
            break
        
        other_hosts.append(scan_network(other_ip))
    
    context = {'ports': ports, 'os': system(), 'ip': my_ip, 'others': other_hosts}
    return render(request, 'localpage/localhost.html', {'context': dumps(context)})