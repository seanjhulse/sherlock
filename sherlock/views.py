from django.shortcuts import render
from django.http import HttpResponse
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
    packet = sock.recvfrom(port)
    
    # Get data from the packet tuple
    data = packet[0]

    # Get IP Address from the packet tuple
    ip_address = packet[1][0]

    # Close the socket
    sock.close()

    # Return the data in a basic HttpResponse
    return HttpResponse("You're getting network traffic %s on port %s:%s" % (data, ip_address, port))



    def local_ports(end_port=1024):
    """Gets network traffic from a port and returns its data
    
            eg. /local-ports{MAX_PORT}

    Args:
        request (Object): [description]
        port (int): the port (0 - 65535)

    Returns:
        HttpResponse: an HTTP response of packet data for the request
    """

    if int(MAX_PORT) > 65535 or int(port) < 0:
        return HttpResponse("Invalid port number: %s." % port)
    open_ports = []

    for port in range(0,end_port):
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = test_socket.connect_ex(("127.0.0.1", port))

        if result == 0:
            open_ports.append(port)
        test_socket.close()

        output = "Open Ports: " + ",".join(str(i) for i in open_ports)

    return HttpResponse(output)
