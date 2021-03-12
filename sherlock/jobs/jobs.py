from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, register_job
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from django.db import transaction
from sherlock.models import Packet

import schedule
import sys
import time
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

def start():
    # run this job every 1 seconds
    register_events(scheduler)
    scheduler.add_job(network_job)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)