from django.shortcuts import render, redirect

def home(request):
    user_type = "" 
    if request.user.is_authenticated:
        user_type = request.user.user_type
    return render(request, 'home.html', {'user_type': user_type})


