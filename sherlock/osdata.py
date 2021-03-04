import nmap3
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
    results = {}
    for ip in ips:
        detection_dict = nmap.nmap_os_detection(ip)
        results.update({ip: detection_dict[ip]['osmatch']})
    # returns dictionary in form {'private IP address' : os information dictionary}
    return results




