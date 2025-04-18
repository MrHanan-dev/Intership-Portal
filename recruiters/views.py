from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import RecruiterProfile
from .forms import RecruiterProfileForm
from users.models import User
from users.decorators import admin_required

class RecruiterListView(ListView):
    model = User
    template_name = 'recruiters/recruiter_list.html'
    context_object_name = 'recruiters'
    
    def get_queryset(self):
        return User.objects.filter(role=User.RECRUITER)

class RecruiterDetailView(DetailView):
    model = User
    template_name = 'recruiters/recruiter_detail.html'
    context_object_name = 'recruiter'
    
    def get_queryset(self):
        return User.objects.filter(role=User.RECRUITER)

class RecruiterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RecruiterProfile
    form_class = RecruiterProfileForm
    template_name = 'recruiters/recruiter_form.html'
    success_url = reverse_lazy('recruiter-list')
    
    def test_func(self):
        return self.request.user.is_admin()