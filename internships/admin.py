from django.contrib import admin
from .models import Internship, Application

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 1

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'company', 'application_deadline')
    inlines = [ApplicationInline]

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'internship', 'status', 'applied_at')
    list_filter = ('status',)