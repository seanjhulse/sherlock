import socket, sys
from struct import *

from django.utils import timezone
from sherlock.models import Packet

# Source: https://www.binarytides.com/python-packet-sniffer-code-linux/
class SocketSniffer:

    def __init__(self):
        # create a AF_PACKET type raw socket (thats basically packet level)
        # define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */
        self.sock = socket.socket(socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))

    def eth_addr(self, address):
        """
        Convert a string of 6 characters of ethernet address into a dash separated hex string

        Args:
            address (str): a 6 char eth address

        Returns:
            str: hex string
        """
        eth_address = "%x:%x:%x:%x:%x:%x" % unpack("BBBBBB", address)
        return eth_address

    def receive_packet(self):
        """
        Receive a packet from the network card

        Returns:
            Packet: a Packet model instance
        """
        packet = self.sock.recvfrom(65565)
        
        # packet string from tuple
        packet = packet[0]
        
        # parse ethernet header
        eth_length = 14
        
        eth_header = packet[:eth_length]
        eth = unpack('!6s6sH' , eth_header)
        eth_protocol = socket.ntohs(eth[2])
        # print('Destination MAC : ' + self.eth_addr(packet[0:6]) + ' Source MAC : ' + self.eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol))

        # Parse IP packets, IP Protocol number = 8
        if eth_protocol == 8 :
            # Parse IP header
            # take first 20 characters for the ip header
            ip_header = packet[eth_length:20+eth_length]
            
            # now unpack them
            iph = unpack('!BBHHHBBH4s4s' , ip_header)

            version_ihl = iph[0]
            version = version_ihl >> 4
            ihl = version_ihl & 0xF

            iph_length = ihl * 4

            ttl = iph[5]
            protocol = iph[6]
            s_addr = socket.inet_ntoa(iph[8]);
            d_addr = socket.inet_ntoa(iph[9]);

            # TCP protocol
            if protocol == 6 :
                t = iph_length + eth_length
                tcp_header = packet[t:t+20]

                #now unpack them :)
                tcph = unpack('!HHLLBBHHH' , tcp_header)
                
                source_port = tcph[0]
                dest_port = tcph[1]
                sequence = tcph[2]
                acknowledgement = tcph[3]
                doff_reserved = tcph[4]
                tcph_length = doff_reserved >> 4
                                
                h_size = eth_length + iph_length + tcph_length * 4
                data_size = len(packet) - h_size
                
                # get data from the packet
                data = packet[h_size:]

                packet = Packet(source_ip_address=s_addr, destination_ip_address=d_addr, header_length=iph_length, ttl=ttl, protocol=protocol, source_port=source_port, destination_port=dest_port, acknowledgement=acknowledgement, payload=data, pub_date=timezone.now())
                
                return packet
                
            # ICMP Packets
            elif protocol == 1 :
                u = iph_length + eth_length
                icmph_length = 4
                icmp_header = packet[u:u+4]

                #now unpack them :)
                icmph = unpack('!BBH' , icmp_header)
                
                icmp_type = icmph[0]
                code = icmph[1]
                checksum = icmph[2]
                
                # print('Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum))
                
                h_size = eth_length + iph_length + icmph_length
                data_size = len(packet) - h_size
                
                #get data from the packet
                data = packet[h_size:]

                # TODO: FINISH AN ICMP PACKET?
                return None
                
            # UDP packets
            elif protocol == 17 :
                u = iph_length + eth_length
                udph_length = 8
                udp_header = packet[u:u+8]

                #now unpack them :)
                udph = unpack('!HHHH' , udp_header)
                
                source_port = udph[0]
                dest_port = udph[1]
                length = udph[2]
                checksum = udph[3]
                
                # print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum))
                
                h_size = eth_length + iph_length + udph_length
                data_size = len(packet) - h_size
                
                # get data from the packet
                data = packet[h_size:]

                packet = Packet(source_ip_address=s_addr, destination_ip_address=d_addr, header_length=iph_length, ttl=ttl, protocol=protocol, source_port=source_port, destination_port=dest_port, payload=data, pub_date=timezone.now())
                return packet
                