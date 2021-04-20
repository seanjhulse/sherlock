from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, register_job
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from django.db import transaction
from sherlock.models import Packet, Scan
import schedule, sys, time, json, nmap
from ..osdata import get_ip
from ..socket_sniffer import SocketSniffer

socket_sniffer = SocketSniffer()

scheduler = BackgroundScheduler()

@register_job(scheduler, 'interval', minutes=5, name='scan network', id="scan network", replace_existing=True)
def nmap_job():
    ip = get_ip()
    cidr = ip + "/24"
    nm = nmap.PortScanner()
    scan_results = nm.scan(hosts=cidr, arguments='-sP')

    scan = Scan(command=scan_results['nmap']['command_line'], scan=json.dumps(scan_results), pub_date=timezone.now())

    try:
        scan.save()
    except Exception as e:
        print("Failed to save latest scan: ", e)


def start():
    # run this job every 1 seconds
    register_events(scheduler)
    # scheduler.add_job(network_job)
    scheduler.add_job(nmap_job)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)