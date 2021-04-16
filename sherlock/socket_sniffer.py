import socket, os, struct, binascii, sys, time
import collections
from django.utils import timezone
from sherlock.models import Packet
from scapy.all import sniff, load_layer
from dns import resolver,reversename

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
        self.packets = collections.deque(maxlen=100)

    def get_packets(self):
        packets = []

        while True:
            try:
                packet = self.packets.popleft()
                if packet is not None:
                    packets.append(packet)
            except IndexError as e:
                break
        
        return packets

    def http_header(self, packet):
        http_packet = str(packet)
        if http_packet.find('GET'):
            return self.GET_print(packet)
    
    def get_host(self, ip):
        try:
            data = socket.gethostbyaddr(ip)
            host = repr(data[0])
            return host
        except Exception:
            # fail gracefully
            return None

    def GET_print(self, packet):
        ret = "***************************************GET PACKET****************************************************\n"
        ret += "\n".join(packet.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
        ret += "*****************************************************************************************************\n"
        return ret

    def packet_callback(self, packet):

        try:
            pkt = Packet()
            packet = packet[0][1]
            
            # IP Address limited to 39 characters
            pkt.source_ip_address = packet.src
            pkt.destination_ip_address = packet.dst
            
            pkt.source_host_name = self.get_host(pkt.source_ip_address)
            pkt.destination_host_name = self.get_host(pkt.destination_ip_address)

            # Time to Live
            pkt.ttl = packet.ttl

            # Protocol
            protocol = packet.proto
            if protocol == TCP:
                pkt.protocol = "TCP"
            if protocol == UDP:
                pkt.protocol = "UDP"

            # Source and Destination Port limited to 5 characters
            pkt.source_port = packet.sport
            pkt.destination_port = packet.dport

            # TCP Flags
            if 'TCP' in packet:
                F = packet['TCP'].flags    # this should give you an integer
                if F & FIN:
                    pkt.flags = "FIN"
                if F & SYN:
                    pkt.flags = "SYN"

            # Payload is just an large TextField representing the body of a message
            if 'Raw' in packet:
                pkt.payload = packet['Raw'].load

                # Attempt to parse the load and - if successful - replace payload with it
                parsed_data = self.http_header(packet)
                if 'Location' in parsed_data:
                    pkt.payload = parsed_data
            else:
                pkt.payload = ""

            # Save the timestamp
            pkt.pub_date = timezone.now()

            # Should store when this data was published to the database
            self.packets.append(pkt)
        except:
            pass

    def sniff_packets(self):
        sniff(prn=self.packet_callback, store=0)