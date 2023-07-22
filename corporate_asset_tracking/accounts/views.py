from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from asset_logs.models import Company, UserProfile
from django.views import View
from .forms import SignUpForm

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            # Check if the company already exists or create a new one
            company, created = Company.objects.get_or_create(name=company_name)
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            # Create the UserProfile and associate it with the company
            UserProfile.objects.create(user=user, company=company)
            #return redirect('device-log-list')
            return render(request, 'device_log_list.html') #will change later!!!!
        return render(request, 'signup.html', {'form': form})
