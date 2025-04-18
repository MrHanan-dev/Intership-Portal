from django import forms
from .models import RecruiterProfile

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'company_description', 'website', 'location']