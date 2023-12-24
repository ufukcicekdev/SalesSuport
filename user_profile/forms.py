from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import JobSeeker 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from .authorization import JobSeekerBackend  
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        backend = JobSeekerBackend()
        user = backend.authenticate(request=None, username=username, password=password)

        if user is None:
            raise ValidationError("Invalid username or password.")

        if not isinstance(user, JobSeeker):
            raise ValidationError("You are not authorized to login.")

        return cleaned_data

    def get_user(self):
        user = super().get_user()
        return user
    
class JobSeekerRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=254, help_text='Required. Enter a valid email address.')

    def __init__(self, *args, **kwargs):
        super(JobSeekerRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_errors = False 
        self.helper.error_text_inline = False 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))


    class Meta:
        model = JobSeeker  
        fields = ('username', 'email', 'password1', 'password2')



from django import forms
from .models import JobSeeker

class JobSeekerForm(forms.ModelForm):
    
    class Meta:
        model = JobSeeker
        fields = [
            'profile_image',
            'username',
            'first_name',
            'last_name',
            'about',
            'cv', 
            'email', 
            'job_type', 
            'phone_number', 
            'address', 
            'facebook_link',
            'instagram_link',
            'linkedin_link',
            'twitter_link',
            'city', 
            'country', 
            'skills', 
            'hobbies', 
            'education_level', 
            'last_school_attended', 
            'graduation_year', 
            'work_experience'
        ]

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image and profile_image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Maximum file size should be 5MB.")
        return profile_image

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        
        if cv:
            # Checking if the file is a PDF by its extension.
            if not cv.name.endswith('.pdf'):
                raise ValidationError("Please upload only a PDF file for the CV.")
            
            if cv.size > 10 * 1024 * 1024:
                raise ValidationError("Maximum file size should be 10MB.")
        
        return cv




