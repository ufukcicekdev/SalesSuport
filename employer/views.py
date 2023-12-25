from django.contrib.auth import  login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm,EmployerRegistrationForm, EmployerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from employer.models import *
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def dashboard(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        employer = Employer.objects.get(username=request.user.username)
        return render(request, 'employer_profile/dashboard.html', {'employer': employer, 'user_type':user_type})
    else:
        return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
          
            return redirect('employer_dashboard')  
    else:
        form = CustomAuthenticationForm()

    return render(request, 'employer_profile/login.html', {'form': form})



def register_view(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'employer'
            user.is_active = True  
            user.save()
            return redirect('employer_login') 
    else:
        form = EmployerRegistrationForm()
    return render(request, 'employer_profile/register.html', {'form': form}) 


def logout_view(request):
    logout(request)
    messages.success(request,'Logged out')
    return redirect('home')

@login_required
def user_profile_view(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        employer = request.user.employer
        
        if request.method == 'POST' and 'update_profile' in request.POST:
            form = EmployerForm(request.POST, request.FILES, instance=request.user.employer)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been successfully updated.')
                return redirect('employer_profile')
        
        else:
            form = EmployerForm(instance=request.user.employer)
        
        # Şifre değiştirme için form
        if request.method == 'POST' and 'change_password' in request.POST:
            changePass = PasswordChangeForm(request.user, request.POST)
            if changePass.is_valid():
                user = changePass.save()
                update_session_auth_hash(request, user)  
                messages.success(request, 'Your password was successfully updated!')
                return redirect('employer_profile')
        
        else:
            changePass = PasswordChangeForm(request.user)
        
        context = {
            'form': form,
            'employer': employer,
            'changePass': changePass,
            'user_type':user_type
        }
        return render(request, 'employer_profile/employerprofile.html', context)
    else:
        messages.error(request, "You need to be logged in to view this page.")
        return redirect('employer_login')
    

