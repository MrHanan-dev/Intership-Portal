from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse

class User(AbstractUser):
    ADMIN = 'admin'
    RECRUITER = 'recruiter'
    STUDENT = 'student'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (RECRUITER, 'Recruiter'),
        (STUDENT, 'Student'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    
    def is_admin(self):
        return self.role == self.ADMIN
    
    def is_recruiter(self):
        return self.role == self.RECRUITER
    
    def is_student(self):
        return self.role == self.STUDENT

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.university}"