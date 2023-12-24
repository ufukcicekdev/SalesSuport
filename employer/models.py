from django.db import models
from mainapp.models import CustomUser
from django.contrib.auth.models import Group, Permission

# Create your models here.


class Employer(CustomUser):
    # İşverenlere özgü alanlar
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    
    
    # Şirket Bilgileri
    founded_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mission_statement = models.TextField(blank=True, null=True)
    
    # Şirket Logo
    company_logo = models.ImageField(upload_to='employer_logos/', blank=True, null=True)
    
    # İş İlanları
    posted_jobs = models.ManyToManyField('Job', blank=True, related_name='related_employers')



class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    
    # İş ilanı için oluşturulmuş sahibi (Employer)
    employer = models.ForeignKey(Employer, related_name='related_jobs', on_delete=models.CASCADE)