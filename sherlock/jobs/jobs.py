from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, register_job
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from django.db import transaction
from sherlock.models import Packet, Scan

import schedule
import sys
import time
import nmap
import json
from ..osdata import get_ip
from ..socket_sniffer import SocketSniffer

socket_sniffer = SocketSniffer()

scheduler = BackgroundScheduler()

@register_job(scheduler, 'interval', seconds=1, name='sniff network traffic', id="sniff network traffic", replace_existing=True)
def network_job():
    packet = socket_sniffer.receive_packet()
    if packet != None and packet.source_ip_address != "127.0.0.1" and packet.destination_ip_address != "127.0.0.1":
        # Lets skip port 53 since that's 99% just DNS calls?
        if packet.source_port != '53' and packet.destination_port != '53': 
            packet.save()

@register_job(scheduler, 'interval', minutes=5, name='scan network', id="scan network", replace_existing=True)
def nmap_job():
    ip = get_ip()
    cidr = ip + "/24"
    nm = nmap.PortScanner()
    scan_results = nm.scan(hosts=cidr, arguments='-sP')

    scan = Scan(command=scan_results['nmap']['command_line'], scan=json.dumps(scan_results), pub_date=timezone.now())

    try:
        scan.save()
    except Error as e:
        print("Failed to save latest scan: {}", e)


def start():
    # run this job every 1 seconds
    register_events(scheduler)
    # scheduler.add_job(network_job)
    scheduler.add_job(nmap_job)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)