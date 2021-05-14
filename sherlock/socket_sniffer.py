import socket, os, struct, binascii, sys, time
import collections
from django.utils import timezone
from sherlock.models import Packet
from scapy.all import sniff, load_layer
from dns import resolver,reversename
import traceback
import logging

# FLAGS
FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80

# PROTOCOLS
TCP = 6
UDP = 17

class SocketSniffer:

    def __init__(self):
        load_layer('tls')
        self.packets = collections.deque(maxlen=1000)

    def get_packets(self):
        try:
            packet = self.packets.popleft()
            return self.convert_packet(packet)
        except IndexError as e:
            return None

    def http_header(self, packet):
        http_packet = str(packet)
        if http_packet.find('GET'):
            return self.GET_print(packet)
    
    def get_host(self, ip):
        try:
            data = socket.gethostbyaddr(ip)
            host = data[0]
            return str(host)
        except Exception:
            # fail gracefully
            return None

    def GET_print(self, packet):
        ret = "***************************************GET PACKET****************************************************\n"
        ret += "\n".join(packet.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
        ret += "*****************************************************************************************************\n"
        return ret

    def convert_packet(self, packet):
        try:
            pkt = Packet()
            packet = packet[0][1]
            
            # IP Address limited to 39 characters
            # packet.show()
            if 'IP' in packet:
                pkt.source_ip_address = packet['IP'].src
                pkt.source_host_name = self.get_host(packet['IP'].src)
                pkt.destination_ip_address = packet['IP'].dst
                pkt.destination_host_name = self.get_host(packet['IP'].dst)

                # Time to Live
                pkt.ttl = packet['IP'].ttl

                # Protocol
                protocol = packet['IP'].proto
                if protocol == TCP:
                    pkt.protocol = "TCP"
                if protocol == UDP:
                    pkt.protocol = "UDP"

            # Source and Destination Port limited to 5 characters
            if 'TCP' in packet:
                pkt.source_port = packet['TCP'].sport
                pkt.destination_port = packet['TCP'].dport

            if 'UDP' in packet:
                pkt.source_port = packet['UDP'].sport
                pkt.destination_port = packet['UDP'].dport

            # TCP Flags
            if 'TCP' in packet:
                F = packet['TCP'].flags    # this should give you an integer
                if F == 'FA' or F == 'F':
                    pkt.flags = "FIN"
                if F == 'S' or F == 'SA':
                    pkt.flags = "SYN"

            # Payload is just an large TextField representing the body of a message
            if 'Raw' in packet:
                pkt.payload = packet['Raw'].load

                # Attempt to parse the load and - if successful - replace payload with it
                parsed_data = self.http_header(packet)
                if str(pkt.source_port) == '80':
                    pkt.payload = parsed_data
            else:
                pkt.payload = ""

            # Save the timestamp
            pkt.pub_date = timezone.now()
            
            return pkt
        except Exception as e:
            logging.error(traceback.format_exc())
            return None 
            
    def packet_callback(self, packet):
        try:
            self.packets.append(packet)
        except:
            logging.error(traceback.format_exc())
            pass

    def sniff_packets(self):
        sniff(prn=self.packet_callback, filter="tcp || udp", store=False)
        # sniff(prn=self.packet_callback, filter="tcp", store=False)