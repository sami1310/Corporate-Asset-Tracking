from django.urls import path
from . import views

app_name = 'asset_logs'

urlpatterns = [
    path('device_log_list/', views.device_log_list, name='device_log_list'),
    path('create_device_log/', views.create_device_log, name='create_device_log'),
    
]