import socket, os, struct, binascii, sys, time
import collections
from django.utils import timezone
from sherlock.models import Packet

# Source: https://www.binarytides.com/python-packet-sniffer-code-linux/
class SocketSniffer:

    def __init__(self):
        # create a AF_PACKET type raw socket (thats basically packet level)
        # define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */
        self.sock = socket.socket(socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
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

    def sniff(self):
        while True:
            # time.sleep(0.1)
            sniffed_data = self.sock.recv(2048)
            packet = Packet()
            packet.pub_date = timezone.now()
            data, ip_bool = self.analyze_ether_data(sniffed_data, packet)

            if ip_bool:
                data, data_length, next_proto = self.analyze_ip_header(data, packet)
                
                if next_proto == "TCP":
                    data = self.analyze_tcp_header(data, data_length, packet)
                    self.packets.append(packet)

                elif next_proto == "UDP":
                    # TODO: Return UDP packets
                    data = self.analyze_udp_header(data, data_length, packet)

    def analyze_tcp_header(self, data, data_length, packet):
        tcp_hdr = struct.unpack("!2H2I4H", data[:20])

        src_port = tcp_hdr[0]
        dst_port = tcp_hdr[1]
        packet.source_port = src_port
        packet.destination_port = dst_port
        
        seq_num = tcp_hdr[2]
        ack_num = tcp_hdr[3]
        packet.sequence_number = seq_num
        packet.acknowledgement = ack_num
        
        data_offset = tcp_hdr[4] >> 12
            
        tcp_data =  data[int(data_offset*4):int(data_length)]
        
        reserved = (tcp_hdr[4] >> 6) & 0x03ff #MUST BE ZERO
        flags = tcp_hdr[4] & 0x003f
        
        urg = flags & 0x0020
        ack = flags & 0x0010
        psh = flags & 0x0008
        rst = flags & 0x0004
        syn = flags & 0x0002
        fin = flags & 0x0001

        if urg:
            packet.urg = True
        if ack:
            packet.ack = True
        if psh:
            packet.psh = True
        if rst:
            packet.rst = True
        if syn:
            packet.syn = True
        if fin:
            packet.fin = True

        window  = tcp_hdr[5]
        checksum = tcp_hdr[6]
        urg_ptr = tcp_hdr[7]

        # print("|============== TCP  HEADER ==============|")
        # print("\tSource Port:\t%hu"	% src_port)
        # print("\tDest Port:\t%hu"	% dst_port)
        # print("\tSeq Number:\t%hu"	% seq_num)
        # print("\tAck Number:\t%hu"	% ack_num)
        # print("\tFlags:")
        # print("\t\tURG: %d"			% urg)
        # print("\t\tACK: %d"			% ack)
        # print("\t\tPSH: %d"			% psh)
        # print("\t\tRST: %d"			% rst)
        # print("\t\tSYN: %d"			% syn)
        # print("\t\tFIN: %d"			% fin)
        # print("\tWindow Size:\t%hu"	% window)
        # print("\tChecksum:\t%hu"	% checksum)
        # print("\tUrgent:\t\t%hu"	% reserved)
        # print("\tPayload:\n%s"		% tcp_data)

        data = data[int(data_offset*4):]
        packet.payload = data

        return data

    def analyze_udp_header(self, data, data_length, packet):
        udp_hdr = struct.unpack("!4H", data[:8])

        src_port = udp_hdr[0]
        dst_port = udp_hdr[1]
        packet.source_port = src_port
        packet.destination_port = dst_port
        
        length   = udp_hdr[2]
        checksum = udp_hdr[3]
        
        data = data[8:]
        packet.payload = data
        
        udp_data = data[:int(length*4-20)]

        # print("|============== UDP  HEADER ==============|")
        # print("\tSource Port:\t%hu"	% src_port)
        # print("\tDest Port:\t%hu"	% dst_port)
        # print("\tLength:\t\t%hu"	% length)
        # print("\tChecksum:\t%hu"	% checksum)
        # print("\tPayload:\n%s"		% udp_data)

        return data

    def analyze_ip_header(self, data, packet):
        ip_hdr = struct.unpack("!6H4s4s", data[:20]) 
        
        version     = ip_hdr[0] >> 12
        packet.version = version

        ihl         = (ip_hdr[0] >> 8) & 0x0f #00001111
        tos 	    = ip_hdr[0] & 0x00ff
        
        length      = ip_hdr[1]
        packet.header_length = length
        
        ip_id       = ip_hdr[2]
        
        flags       = ip_hdr[3]	>> 13
        frag_offset = ip_hdr[3] & 0x1fff
        
        ip_ttl      = ip_hdr[4] >> 8
        packet.ttl = ip_ttl

        ip_protocol = ip_hdr[4] & 0x00ff
        
        chksum      = ip_hdr[5]
        
        src_addr    = socket.inet_ntoa(ip_hdr[6])
        dst_addr   = socket.inet_ntoa(ip_hdr[7])
        packet.source_ip_address = src_addr
        packet.destination_ip_address = dst_addr

        try:
            packet.source_host_name = socket.gethostbyaddr(src_addr)[0]
            packet.destination_host_name = socket.gethostbyaddr(dst_addr)[0]
        except:
            # print("Failed to resolve hostname. Source {}, Destination {}", src_addr, dst_addr)
            pass
        
        no_frag = flags >> 1
        more_frag = flags & 0x1
        #Portocol table
        table = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
        try:
            proto_name = "(%s)" % table[ip_protocol]
        except:
            proto_name = ""

        # print("|=============== IP HEADER ===============|")
        # print("\tVersion:\t%hu" 	% version)
        # print("\tIHL:\t\t%hu" 		% ihl)
        # print("\tTOS:\t\t%hu" 		% tos)
        # print("\tID:\t\t%hu" 		% ip_id)
        # print("\tNo Frag:\t%hu"		% no_frag)
        # print("\tMore frag:\t%hu"	% more_frag)
        # print("\tOffset:\t\t%hu"		% frag_offset)
        # print("\tTTL:\t\t%hu"		% ip_ttl)
        # print("\tNext protocol:\t%hu%s"	% (ip_protocol, proto_name))
        # print("\tChecksum:\t%hu"	% chksum)
        # print("\tSource IP:\t%s"	% src_addr)
        # print("\tDest IP:\t%s"	% dst_addr)
        
        if(ip_protocol == 6): #TCP magic number
            next_proto = "TCP"
        elif (ip_protocol == 17): #UDP magic number
            next_proto = "UDP"
        else:
            next_proto = "OTHER"

        data_length = length-(ihl*32)/8
        data = data[int((ihl*32)/8):]
        return data, data_length, next_proto
        
    def analyze_ether_data(self, data, packet):
        ip_bool = False
        
        eth_hdr = struct.unpack("!6s6sH", data[:14]) 
        dest_mac = binascii.hexlify(eth_hdr[0]) # Destination address
        src_mac  = binascii.hexlify(eth_hdr[1]) # Source address
        protocol  = eth_hdr[2] >> 8 # Next Protocol 

        # print("|============ ETHERNET HEADER ============|")
        # print("|Destination MAC:\t%s:%s:%s:%s:%s:%s" % (dest_mac[0:2],
        #         dest_mac[2:4],dest_mac[4:6],dest_mac[6:8],dest_mac[8:10],dest_mac[10:12]))
        # print("|Source MAC:\t\t%s:%s:%s:%s:%s:%s" % (src_mac[0:2],
        #         src_mac[2:4],src_mac[4:6],src_mac[6:8],src_mac[8:10],src_mac[10:12]))
        # print("|Protocol:\t\t%hu" % protocol)
                
        if(protocol == 8): #IPv4 = 0x0800
            ip_bool = True
        
        packet.protocol = protocol

        data = data[14:]
        return data, ip_bool