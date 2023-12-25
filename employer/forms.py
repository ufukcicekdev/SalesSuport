from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from employer.models import Employer 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from .authorization import EmployerBackend


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        backend = EmployerBackend()
        user = backend.authenticate(request=None, username=username, password=password)

        if user is None:
            raise ValidationError("Invalid username or password.")

        if not isinstance(user, Employer):
            raise ValidationError("You are not authorized to login.")

        return cleaned_data

    def get_user(self):
        user = super().get_user()
        return user
    
class EmployerRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=254, help_text='Required. Enter a valid email address.')

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_errors = False 
        self.helper.error_text_inline = False 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))


    class Meta:
        model = Employer  
        fields = ('username', 'email', 'password1', 'password2')





class EmployerForm(forms.ModelForm):
    
    class Meta:
        model = Employer
        fields = [
            'username',
            'first_name',
            'last_name',
            'email', 
            'user_type', 
            'phone_number', 
            'address', 
            'facebook_link',
            'instagram_link',
            'linkedin_link',
            'twitter_link',
            'city', 
            'country', 
        ]

  



