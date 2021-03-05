from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /example/5/
    path('example/<int:id>/', views.detail, name='detail'),
    path('network-traffic/<int:port>/', views.network_traffic, name='network-traffic'),
    path('network-os/', views.network_operating_systems, name='network-os')
]