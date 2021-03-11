from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /example/5/
    path('example/<int:id>/', views.detail, name='detail'),
    path('example/websockets', views.web_sockets_example, name='web_sockets_example'),
    path('network-traffic/<int:port>/', views.network_traffic, name='network-traffic'),
    path('network-os/', views.network_operating_systems, name='network-os'),
	path('host-scan-all/<str:ipaddress>/', views.host_scan_all, name='host-scan-all'),
	path('host-scan/<str:ipaddress>/<str:portrange>', views.host_scan, name='host-scan'),
    path('local-ports/', views.local_ports, name="local-ports"),
]