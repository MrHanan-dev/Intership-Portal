# internship_portal/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, StudentProfile
from internships.models import Internship, Application
from recruiters.models import RecruiterProfile

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'
    fk_name = 'user'

class RecruiterProfileInline(admin.StackedInline):
    model = RecruiterProfile
    can_delete = False
    verbose_name_plural = 'Recruiter Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (StudentProfileInline, RecruiterProfileInline)
    list_display = ('username', 'email', 'role', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'role')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'company', 'location', 'application_deadline', 'created_at')
    list_filter = ('application_deadline', 'created_at', 'location')
    search_fields = ('title', 'company', 'description')
    raw_id_fields = ('recruiter',)
    date_hierarchy = 'application_deadline'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Company Info', {'fields': ('recruiter', 'company', 'location')}),
        ('Dates', {'fields': ('application_deadline',)}),
    )

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'internship', 'status', 'applied_at', 'updated_at')
    list_filter = ('status', 'applied_at', 'updated_at')
    search_fields = ('student__username', 'internship__title')
    raw_id_fields = ('student', 'internship')
    date_hierarchy = 'applied_at'
    ordering = ('-applied_at',)
    fieldsets = (
        (None, {'fields': ('student', 'internship')}),
        ('Application Details', {'fields': ('cover_letter', 'resume', 'status')}),
    )

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'location', 'website')
    search_fields = ('company_name', 'user__username', 'location')
    list_filter = ('location',)
    raw_id_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Company Info', {'fields': ('company_name', 'company_description', 'website', 'location')}),
    )

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'major', 'graduation_year')
    search_fields = ('user__username', 'university', 'major')
    list_filter = ('graduation_year', 'university')
    raw_id_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Education Info', {'fields': ('university', 'major', 'graduation_year')}),
        ('Bio', {'fields': ('bio',)}),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Internship, InternshipAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(RecruiterProfile, RecruiterProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)