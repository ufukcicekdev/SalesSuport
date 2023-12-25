from django.urls import path, include
from django.conf.urls import handler404, handler500
from employer.views import *

urlpatterns = [
    # ... diğer URL tanımlamaları
    path('employer_login/', login_view, name='employer_login'),
    path('employer_register/',register_view, name='employer_register'),
    path('employer_dashboard/',dashboard, name='employer_dashboard'),
    path('employer_logout/',logout_view,name="employer_logout"),
    path('employer_profile/',user_profile_view,name="employer_profile"),

]