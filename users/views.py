from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db import transaction
from .models import User, StudentProfile
from recruiters.models import RecruiterProfile
from .forms import UserSignupForm
from .decorators import admin_required, recruiter_required, student_required

def home(request):
    return render(request, 'home.html')

class SignUpView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'users/signup.html'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        
        # Create profile based on user role
        if user.role == User.STUDENT:
            StudentProfile.objects.create(
                user=user,
                university=form.cleaned_data.get('university'),
                major=form.cleaned_data.get('major'),
                graduation_year=form.cleaned_data.get('graduation_year')
            )
        elif user.role == User.RECRUITER:
            RecruiterProfile.objects.create(
                user=user,
                company_name=form.cleaned_data.get('company_name'),
                company_description=form.cleaned_data.get('company_description'),
                website=form.cleaned_data.get('website'),
                location=form.cleaned_data.get('location')
            )
        
        login(self.request, user)
        return redirect('dashboard')

@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}
    
    if user.is_admin():
        return render(request, 'users/admin_dashboard.html', context)
    elif user.is_recruiter():
        return render(request, 'users/recruiter_dashboard.html', context)
    else:  # Student
        return render(request, 'users/student_dashboard.html', context)