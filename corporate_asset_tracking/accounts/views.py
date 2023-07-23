#from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
#from asset_logs.models import Company, UserProfile
#from django.views import View
#from .forms import SignUpForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from asset_logs.models import Company, UserProfile, DeviceLog
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            company_name = request.POST.get('company_name')

            # Check if the company already exists in the Company model
            try:
                company = Company.objects.get(name=company_name)
            except Company.DoesNotExist:
                company = Company(name=company_name)
                company.save()

            # Create a new user and link it to the company
            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile(user=user, company=company)
            user_profile.save()

            # Redirect to the login page after successful signup
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('asset_logs:device_log_list')
        else:
            # Handle invalid login credentials
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')

    else:
        logout(request)
        return redirect('accounts:login')
