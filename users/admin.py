from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [StudentProfileInline]
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(User, CustomUserAdmin)