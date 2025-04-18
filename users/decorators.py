# users/decorators.py
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from functools import wraps
from internships.models import Internship

def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the logged-in user is an admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_admin(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def recruiter_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the logged-in user is a recruiter.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_recruiter(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the logged-in user is a student.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_student(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def recruiter_or_admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the logged-in user is either a recruiter or an admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_recruiter() or u.is_admin()),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def can_edit_internship(view_func):
    """
    Decorator that checks if the user can edit the internship.
    Admins can edit any internship, recruiters can only edit their own.
    """
    @wraps(view_func)
    def wrapper(request, internship_id, *args, **kwargs):
        internship = get_object_or_404(Internship, id=internship_id)
        
        # Admin can edit any internship
        if request.user.is_admin():
            return view_func(request, internship_id, *args, **kwargs)
        
        # Recruiter can only edit their own internships
        if request.user.is_recruiter() and internship.recruiter == request.user:
            return view_func(request, internship_id, *args, **kwargs)
        
        return HttpResponseForbidden("You don't have permission to edit this internship.")
    
    return wrapper