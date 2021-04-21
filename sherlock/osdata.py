import nmap
import nmap3 # if you don't have nmap3, either run pip install python3-nmap or just comment this line and list_os() method out
import os
import re
import socket
import subprocess
import multiprocessing

# deprecated method,must refactor at a later date
def list_os():
    ips = map_net()
    nmap3 = nmap.Nmap()
    ips_os = {}
    
    for ip in ips:
        detection_dict = nmap.nmap_os_detection(ip)
        ips_os.update({ip: detection_dict[str(ip)]['osmatch'][0]})
    
    # returns dictionary in form {'private IP address' : os information dictionary}

    for ip, os_info in ips_os.items():
        print(f'Ip address: {ip}, os info: {os_info}')
    
    return ips_os


def pinger(workq, resq):
    DEVNULL = open(os.devnull, 'w')
    while True:
        ip = workq.get()
        if ip is None:
            break
        try:
            subprocess.check_call(['ping', '-c1', ip], stdout=DEVNULL)
            resq.put(ip)
        except:
            pass

def map_net(pool_size=255):
    ip_list = []
    ip_parts = get_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]
    for p in pool:
        p.start()
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))
    for p in pool: 
        jobs.put(None)
    for p in pool:
        p.join()
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)
    return ip_list

def get_op_sys(ip_list):
    scanner = nmap.PortScanner()
    res = []
    for ip in ip_list:
        res.append(scanner.scan(ip, arguments="-O")['scan'])
    
    return res

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally: 
        s.close()
    return ip

def scan_network(ip):
    nm = nmap.PortScanner()
    return nm.scan(hosts=ip, arguments='-O -T5 -n --max-parallelism=255 --min-parallelism=100')

def get_vendor(ip):
    nmap = nmap3.Nmap()
    os_results = nmap.nmap_os_detection(ip)
    try:
        return os_results[ip]['osmatch'][0]['osclass']['osfamily']
    except KeyError:
        return 'default' 