from django.contrib.auth.backends import ModelBackend
from .models import Employer

class BaseBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.model.objects.get(username=username)
            if user.check_password(password) and self.check_user_type(user):
                return user
        except self.model.DoesNotExist:
            return None

    def check_user_type(self, user):
        return True  
    

class EmployerBackend(BaseBackend):
    model = Employer 

    def check_user_type(self, user):
        return isinstance(user, Employer)

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.model.objects.get(username=username)
            if user.check_password(password) and self.check_user_type(user):
                return user
        except self.model.DoesNotExist:
            return None

# class EmployerBackend(BaseBackend):
#     def check_user_type(self, user):
#         return isinstance(user, Employer)

# class CompanyBackend(BaseBackend):
#     def check_user_type(self, user):