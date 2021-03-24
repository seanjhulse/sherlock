from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from sherlock.models import Packet

import socket
import nmap
from .osdata import list_os

# Views
def index(request):
	return render(request, 'homepage/index.html')

def node_map(request):
    return render(request, 'homepage/cytoscape.html', {})

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
    return HttpResponse('The operating systems on this network are: %s' % (list_os()))

def host_scan_all(request, ipaddress):
	""" Scan an ipaddress for other hosts """
	
	nm = nmap.PortScanner()
	
	scan_info = nm.scan(ipaddress)
	
	return HttpResponse("Other hosts found: %s" % (scan_info['scan']))

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

    return HttpResponse(",".join(str(i) for i in open_ports))

def web_sockets_example(request):
    """Provides a sample websocket connection

    Args:
        request (request): renders a simple web socket application

    Returns:
        HTML
    """
    return render(request, 'examples/websockets/index.html')
