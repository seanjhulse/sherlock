from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.core import serializers
from django.forms.models import model_to_dict
from sherlock.models import Packet

from sherlock.models import Packet, Scan
from platform import system
import datetime
import socket
import nmap

from .osdata import get_op_sys, get_ip, map_net, scan_network, get_vendor
import pyufw as ufw


import json

# Views
def index(request):
	return render(request, 'homepage/index.html')

def node_map(request):
    my_ip = get_ip()
    context = {'ip': my_ip, 'os': system()}
    return render(request, 'homepage/node-map.html', {'context': json.dumps(context)})

def delete_all(request):
    Packet.objects.all().delete()
    return JsonResponse({"message": "Nodes deleted"})

def get_nodes(request, minutes=5):
    packetTime = timezone.now() - datetime.timedelta(minutes=minutes)
    # Filter packets based on pub_date (__gte == any date greater than or equal to)
    nodes = Packet.objects.filter(pub_date__gte=packetTime).values()
    return JsonResponse({"nodes": list(nodes)})

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


def network_operating_systems(request, ip):
    ''' I tried getting the following working but there were issues, namely:
        1. The os scan process using nmap or nmap3 slowed down the node map considerably
        2. Inaccurate results would come back for mostly every other node that wasn't on a local network
    '''
    # 
    # vendor = get_vendor(ip)
    vendor = 'default'
    return HttpResponse(vendor)
    # return HttpResponse('The operating systems on this network are: %s' % (get_op_sys(map_net())))

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


def local_ports(request, ip="127.0.0.1", portrange=65535):
    """Scan all local ports 

    Args: 
       request (Object): [description]
    Returns:
      comma separated list in HttpResponse
    """
    open_ports = []

    for port in range(0,portrange):
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = test_socket.connect_ex((ip, port))

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
    
def localpage(request, ajaxip):
    print('Scanning for other hosts...')
    ports = []
    ports = json.dumps(ports)
    cidr = ajaxip + "/24"
    nm = nmap.PortScanner()
    scan_results = nm.scan(hosts=cidr, arguments='-sP')
    scan = json.dumps(scan_results) 
    print('finished scanning for other hosts')

    print(scan)
    my_ip = ajaxip
    
    latest_scan = Scan.objects.last()
    context = {'ports': ports, 'os': system(), 'ip': my_ip, 'scan': json.loads(scan)}
    return render(request, 'localpage/localhost.html', {'context': json.dumps(context)})


def portpage(request, ajaxip):
    print('Getting ports...')

    ports = local_ports(request)
    my_ip = ajaxip
    ports = json.dumps(ports)
    context = {'ports': ports, 'os': system(), 'ip': my_ip }
    return render(request, 'host-node/host-node.html', {'context' : json.dumps(context)})


def splash_page(request):
    return render(request, 'homepage/splash-page.html')

def tutpage1(request):
    return render(request, 'tutorial/tutpage1.html')

def tutpage2(request):
    return render(request, 'tutorial/tutpage2.html')

def tutpage3(request):
    return render(request, 'tutorial/tutpage3.html')

def tutpage4(request):
    return render(request, 'tutorial/tutpage4.html')

def tutpage5(request):
    return render(request, 'tutorial/tutpage5.html')

def ufw_block(request,blocktype,blocktarget):

    if (blocktype == "in") | (blocktype == "out"):
        ufw.add("deny " + blocktype + " " + blocktarget)

    elif blocktype == "host":
        ufw.add("deny from " + blocktarget + " to any")

    if ufw.status() == "active":
        ufw.reload()
    elif ufw.status() == "inactive":
        ufw.enable()
    return HttpResponse("Block Successful");

def ufw_manager(request):
    ufw_rules = ufw.status()['rules'];

    context = {'rules': ufw_rules}

    return render(request, 'homepage/ufw-manager.html', {'context' : json.dumps(context)})

def ufw_delete_rule(request, rule):

    ufw.delete(rule)
    return HttpResponse("Delete Successful");

