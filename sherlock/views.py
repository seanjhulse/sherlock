from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from sherlock.models import Packet

import nmap
from .osdata import list_os
from .socket_sniffer import SocketSniffer 

# Constants
MAX_PORT = 65535

# Views
def index(request):
    return HttpResponse("Hello, world. You're at the sherlock index.")

def detail(request, id):
    """This is an example end point which takes an "id" and returns it.

    Args:
        request (Object): request object
        object (int): object id

    Returns:
        HttpResponse: an HTTP response of the id in the request
    """
    return HttpResponse("You're looking at object %s." % id)

def network_traffic(request):
    """Gets network traffic
    
    Args:
        request (Object): [description]

    Returns:
        HttpResponse: an HTTP response of packet data for the request
    """
    sniffer = SocketSniffer()
    packet = sniffer.receive_packet()
    
    # Return the data in a basic HttpResponse
    return HttpResponse("You're getting network traffic")
    # return HttpResponse("You're getting network traffic %s on port %s:%s" % (packet.payload, packet.host_ip_address, packet.port))


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


def web_sockets_example(request):
    """Provides a sample websocket connection

    Args:
        request (request): renders a simple web socket application

    Returns:
        HTML
    """
    return render(request, 'examples/websockets/index.html')