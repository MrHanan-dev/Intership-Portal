from django.db import models
from django.conf import settings

class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.username} - {self.company_name}"
