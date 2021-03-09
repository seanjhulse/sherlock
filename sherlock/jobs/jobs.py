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
    packet.save()

def start():
    # run this job every 60 seconds
    register_events(scheduler)
    scheduler.add_job(network_job)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)