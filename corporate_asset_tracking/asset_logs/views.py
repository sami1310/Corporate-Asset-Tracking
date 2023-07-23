#from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.views.generic import ListView
#from .models import DeviceLog, UserProfile
#from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from .models import DeviceLog, Company, UserProfile 
from django.contrib.auth.decorators import login_required
from .forms import DeviceLogForm

@login_required
def device_log_list(request):
    user_company = request.user.userprofile.company
    device_logs = DeviceLog.objects.filter(employee__company=user_company)
    return render(request, 'device_log_list.html', {'device_logs': device_logs})


@login_required
def create_device_log(request):
    user_company = request.user.userprofile.company

    if request.method == 'POST':
        form = DeviceLogForm(request.POST)

        if form.is_valid():
            device_log = form.save(commit=False)
            device_log.employee = request.user.userprofile
            device_log.company = user_company
            device_log.save()
            return redirect('asset_logs:device_log_list')
    else:
        form = DeviceLogForm()

    return render(request, 'create_device_log.html', {'form': form})