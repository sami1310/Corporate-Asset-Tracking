from django.urls import path
from . import views

app_name = 'asset_logs'

urlpatterns = [
    path('device_log_list/', views.device_log_list, name='device_log_list'),
    # other URL patterns
]