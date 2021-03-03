from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from sherlock.models import Packet

import socket

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

def network_traffic(request, port):
    """Gets network traffic from a port and returns its data
    
    eg. /network-traffic/{PORT}

    Args:
        request (Object): [description]
        port (int): the port (0 - 65535)

    Returns:
        HttpResponse: an HTTP response of packet data for the request
    """

    if int(MAX_PORT) > 65535 or int(port) < 0:
        return HttpResponse("Invalid port number: %s." % port)

    # create INET socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    # recieve packet
    raw_packet = sock.recvfrom(port)

    # Close the socket
    sock.close()
    
    # Get data from the packet tuple
    data = raw_packet[0]

    # Get IP Address from the packet tuple
    host_ip_address = raw_packet[1][0]

    # Create a packet object and save it to the database
    packet = Packet(host_ip_address=host_ip_address, dest_ip_address="localhost", port=port, payload=data, pub_date=timezone.now())
    packet.save()

    # Return the data in a basic HttpResponse
    return HttpResponse("You're getting network traffic %s on port %s:%s" % (packet.payload, packet.host_ip_address, packet.port))