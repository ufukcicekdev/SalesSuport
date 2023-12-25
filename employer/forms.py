from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from employer.models import Employer 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from .authorization import EmployerBackend
from django.core.validators import URLValidator
from mainapp.utils import validate_social_link

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
            'company_logo',
            'username',
            'company_name',
            'industry',
            'founded_date',
            'description',
            'mission_statement',
            'email', 
            'phone_number', 
            'address', 
            'website',
            'facebook_link',
            'instagram_link',
            'linkedin_link',
            'twitter_link',
            'city', 
            'country', 
        ]

    company_name = forms.CharField(required=True, label='Company Name')
    industry = forms.CharField(required=True, label='Industry')
    description = forms.CharField(required=True, widget=forms.Textarea, label='Description')
    mission_statement = forms.CharField(required=True, widget=forms.Textarea, label='Mission Statement')
    email = forms.EmailField(required=True, label='Email')
    phone_number = forms.CharField(required=True, label='Phone Number')
    website = forms.URLField(required=True, label='Website')
    city = forms.CharField(required=True, label='City')

    def clean_profile_image(self):
        company_logo = self.cleaned_data.get('company_logo')
        if company_logo and company_logo.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Maximum file size should be 5MB.")
        return company_logo
  
    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website:
            url_validator = URLValidator()
            try:
                url_validator(website)
            except ValidationError:
                raise forms.ValidationError("Please enter a valid website URL.")
        return website

    

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



