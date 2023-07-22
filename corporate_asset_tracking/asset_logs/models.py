from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 
    

class Device(models.Model):
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    device_type = models.CharField(max_length=10, blank= False)
    device_model = models.CharField(max_length=10, blank= False)
   
    
class DeviceLog(models.Model):
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    checked_out_date = models.DateTimeField(null=False, blank=False)
    checked_in_date = models.DateTimeField(null=True, blank=True)
    condition_when_checked_out = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    condition_when_checked_in = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=False)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)