from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, StudentProfile

class UserSignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    
    # Student fields
    university = forms.CharField(max_length=100, required=False)
    major = forms.CharField(max_length=100, required=False)
    graduation_year = forms.IntegerField(required=False)
    
    # Recruiter fields
    company_name = forms.CharField(max_length=100, required=False)
    company_description = forms.CharField(widget=forms.Textarea, required=False)
    website = forms.URLField(required=False)
    location = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == User.STUDENT:
            if not cleaned_data.get('university'):
                self.add_error('university', 'This field is required for students.')
            if not cleaned_data.get('major'):
                self.add_error('major', 'This field is required for students.')
            if not cleaned_data.get('graduation_year'):
                self.add_error('graduation_year', 'This field is required for students.')
        
        elif role == User.RECRUITER:
            if not cleaned_data.get('company_name'):
                self.add_error('company_name', 'This field is required for recruiters.')
            if not cleaned_data.get('company_description'):
                self.add_error('company_description', 'This field is required for recruiters.')
            if not cleaned_data.get('location'):
                self.add_error('location', 'This field is required for recruiters.')
        
        return cleaned_data
