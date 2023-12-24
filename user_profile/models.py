from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from mainapp.models import *




class JobSeeker(CustomUser):
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    NETWORKER = 'NW'
    FREELANCER_SALESPERSON = 'FS'
    FULL_TIME_SALESPERSON = 'FT'
    
    USER_TYPE_CHOICES = [
        (NETWORKER, 'Networker'),
        (FREELANCER_SALESPERSON, 'Freelancer Salesperson'),
        (FULL_TIME_SALESPERSON, 'Full-Time Salesperson'),
    ]
    
    job_type = models.CharField(
        max_length=2,
        choices=USER_TYPE_CHOICES,
        default=NETWORKER,
    )

    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    
    # Eğitim ve Deneyim Bilgileri
    education_level = models.CharField(max_length=100, blank=True, null=True)
    last_school_attended = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)
    
    # Kullanıcı tipine özgü alanlar
    connections = models.ManyToManyField('self', blank=True, related_name='jobseeker_connections')
    projects = models.ManyToManyField('Project', blank=True, related_name='jobseeker_projects')
    sales_performance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


class Project(models.Model):
    # Proje ile ilgili alanlarınızı buraya ekleyin.
    name = models.CharField(max_length=255)





# class SoftwareSeekerCompany(AbstractUser):
#     # Yazılım arayan ve satın alım yapmak isteyen şirketlere özgü alanlar
#     company_name = models.CharField(max_length=255)
#     software_requirements = models.TextField()
#     # Diğer özgü alanlar...