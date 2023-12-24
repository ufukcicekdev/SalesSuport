from django.urls import path,include
from django.conf.urls import handler404, handler500
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('', include('user_profile.urls')),

]