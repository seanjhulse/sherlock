from background_task import background
from django.contrib.sherlock.models import Packet 

from struct import *
import socket
import SocketSniffer

sniffer = SocketSniffer()

@background(schedule=1)
def network_traffic():
    sniffer.receive_packet()