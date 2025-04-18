from django.contrib import admin
from .models import RecruiterProfile

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'location')
    search_fields = ('company_name', 'user__username')