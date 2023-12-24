from django.contrib.auth import  login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm,JobSeekerRegistrationForm, JobSeekerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from employer.models import *
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def dashboard(request):
    if request.user.is_authenticated:
        jobseeker = Employer.objects.get(username=request.user.username)
        return render(request, 'employer_profile/dashboard.html', {'jobseeker': jobseeker})
    else:
        return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
          
            return redirect('dashboard')  
    else:
        form = CustomAuthenticationForm()

    return render(request, 'employer_profile/login.html', {'form': form})



def register_view(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  
            user.save()
            return redirect('login') 
    else:
        form = JobSeekerRegistrationForm()
    return render(request, 'employer_profile/register.html', {'form': form}) 


def logout_view(request):
    logout(request)
    messages.success(request,'Logged out')
    return redirect('home')

@login_required
def user_profile_view(request):
    if request.user.is_authenticated:
        jobseeker = Employer.objects.get(username=request.user.username)
        
        # Profil bilgileri için form
        if request.method == 'POST' and 'update_profile' in request.POST:
            form = JobSeekerForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been successfully updated.')
                return redirect('profile')
        
        else:
            form = JobSeekerForm(instance=request.user)
        
        # Şifre değiştirme için form
        if request.method == 'POST' and 'change_password' in request.POST:
            changePass = PasswordChangeForm(request.user, request.POST)
            if changePass.is_valid():
                user = changePass.save()
                update_session_auth_hash(request, user)  
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
        
        else:
            changePass = PasswordChangeForm(request.user)
        
        context = {
            'form': form,
            'jobseeker': jobseeker,
            'changePass': changePass
        }
        return render(request, 'employer_profile/employerprofile.html', context)
    else:
        messages.error(request, "You need to be logged in to view this page.")
        return redirect('login')
    
