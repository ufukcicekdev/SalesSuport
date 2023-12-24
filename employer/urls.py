from django.urls import path, include
from django.conf.urls import handler404, handler500
from employer.views import *

urlpatterns = [
    # ... diğer URL tanımlamaları
    path('login/', login_view, name='login'),
    path('register/',register_view, name='register'),
    path('dashboard/',dashboard, name='dashboard'),
    path('logout/',logout_view,name="logout"),
    path('profile/',user_profile_view,name="profile"),

]