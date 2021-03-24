from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /example/5/
    path('example/<int:id>/', views.detail, name='detail'),
    path('node-map', views.node_map, name='node-map'),
	path('host-scan', views.host_scan, name='host-scan'),
    path('network-traffic', views.net_traf, name='network-traffic'),
	path('host-scan-all', views.host_scan_all, name='host-scan-all'),
    path('network-os', views.network_operating_systems, name='network-os'),
    path('local-ports/', views.local_ports, name="local-ports"),
]