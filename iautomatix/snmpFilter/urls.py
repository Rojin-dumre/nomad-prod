from django.urls import path

from . import views

urlpatterns = [
	path('snmp-list/', views.snmpList, name='snmp-list'),
    path('snmp-create/', views.snmpCreate, name='snmp-create'),
    path('snmp-detail/<str:pk>/', views.snmpDetail, name='snmp-detail'),
    path('snmp-update/<str:pk>/', views.snmpUpdate, name ='snmp-update'),
    path('snmp-delete/<str:pk>/', views.snmpDelete, name='snmp-delete'),
    path('snmp-tree/<str:host>/', views.snmpTree, name='snmp-tree')


]

