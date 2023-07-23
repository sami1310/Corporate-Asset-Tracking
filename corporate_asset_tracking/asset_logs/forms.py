from django import forms
from .models import DeviceLog

class DeviceLogForm(forms.ModelForm):
    class Meta:
        model = DeviceLog
        fields = ['employee','device', 'checked_out_date', 'condition_when_checked_out','checked_in_date','condition_when_checked_in']