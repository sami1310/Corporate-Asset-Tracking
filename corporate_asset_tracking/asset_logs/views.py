#from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.views.generic import ListView
#from .models import DeviceLog, UserProfile
#from django.shortcuts import get_object_or_404

from django.shortcuts import render
from .models import DeviceLog, Company, UserProfile 
from django.contrib.auth.decorators import login_required

@login_required
def device_log_list(request):
    user_company = request.user.userprofile.company
    device_logs = DeviceLog.objects.filter(employee__company=user_company)
    return render(request, 'device_log_list.html', {'device_logs': device_logs})
