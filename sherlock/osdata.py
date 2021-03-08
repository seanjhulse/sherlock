import nmap
import os
import re


def get_ipaddrs():
    # arp -a normally maps ip addresses to mac addresses, but works for our purposes in listing all ips in LAN (including gateway)
    devices = [device for device in os.popen('arp -a')]
    devices.insert(0, '127.0.0.1')
    ipaddrs = []
    for device in devices:
        # makes sure we only get the ipv4 and not rest of information
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', device)    
        ipaddrs.append(ip[0])
    return ipaddrs


def list_os():
    ips = get_ipaddrs()
    nmap = nmap3.Nmap()
    ips_os = {}
    
    
    for ip in ips:
        detection_dict = nmap.nmap_os_detection(ip)
        ips_os.update({ip: detection_dict[str(ip)]['osmatch'][0]})
    
    # returns dictionary in form {'private IP address' : os information dictionary}

    for ip, os_info in ips_os.items():
        print(f'Ip address: {ip}, os info: {os_info}')
    
    return ips_os
