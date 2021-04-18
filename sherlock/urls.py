from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /example/5/
    path('example/<int:id>/', views.detail, name='detail'),
    path('network-traffic/', views.net_traf, name='network-traffic'),
    path('example/websockets', views.web_sockets_example, name='web_sockets_example'),
    path('localpage/<str:ajaxip>', views.localpage, name='localpage'),
    path('portpage/<str:ajaxip>', views.portpage, name='portpage'),
    path('network-os/', views.network_operating_systems, name='network-os'),
	path('host-scan-all/<str:ipaddress>/', views.host_scan_all, name='host-scan-all'),
	path('host-scan/<str:ipaddress>/<str:portrange>', views.host_scan, name='host-scan'),
    path('local-ports/', views.local_ports, name="local-ports"),
    path('node-map', views.node_map, name='node-map'),
    path('host-node', views.host_node, name='host-node'),
    path('nodes/<int:minutes>/', views.get_nodes, name='get-nodes'),
    path('delete-all/', views.delete_all, name='delete-all'),
    path('splash-page/', views.splash_page, name='splash-page'),
    path('tutpage1/', views.tutpage1, name='tutpage1'),
    path('tutpage2/', views.tutpage2, name='tutpage2'),
    path('tutpage3/', views.tutpage3, name='tutpage3'),
    path('tutpage4/', views.tutpage4, name='tutpage4'),
    path('tutpage5/', views.tutpage5, name='tutpage5'),
]