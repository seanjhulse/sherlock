from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /example/5/
    path('example/<int:id>/', views.detail, name='detail'),
    path('network-traffic', views.net_traf, name='network-traffic'),
    path('network-os', views.network_operating_systems, name='network-os'),
	path('host-scan-all', views.host_scan_all, name='host-scan-all'),
	path('host-scan', views.host_scan, name='host-scan'),
    url('node-map', views.node_map, name='node-map'),
]