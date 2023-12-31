from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import JobSeeker 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from .authorization import JobSeekerBackend  
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from mainapp.utils import validate_social_link


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



    def clean_facebook_link(self):
        facebook_link = self.cleaned_data.get('facebook_link')
        if facebook_link:
            return validate_social_link(facebook_link, "Facebook", "facebook")
        return facebook_link

    def clean_twitter_link(self):
        twitter_link = self.cleaned_data.get('twitter_link')
        if twitter_link:
            return validate_social_link(twitter_link, "Twitter", "twitter")
        return twitter_link

    def clean_linkedin_link(self):
        linkedin_link = self.cleaned_data.get('linkedin_link')
        if linkedin_link:
            return validate_social_link(linkedin_link, "LinkedIn", "linkedin")
        return linkedin_link

    def clean_instagram_link(self):
        instagram_link = self.cleaned_data.get('instagram_link')
        if instagram_link:
            return validate_social_link(instagram_link, "Instagram", "instagram")
        return instagram_link




