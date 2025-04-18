from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from .models import Internship, Application
from .forms import InternshipForm, ApplicationForm
from users.decorators import recruiter_or_admin_required, can_edit_internship, student_required

class InternshipListView(ListView):
    model = Internship
    template_name = 'internships/internship_list.html'
    context_object_name = 'internships'

class InternshipDetailView(DetailView):
    model = Internship
    template_name = 'internships/internship_detail.html'

class InternshipCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Internship
    form_class = InternshipForm
    template_name = 'internships/internship_form.html'
    success_url = reverse_lazy('internship-list')
    
    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_recruiter()
    
    def form_valid(self, form):
        form.instance.recruiter = self.request.user
        return super().form_valid(form)

class InternshipUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Internship
    form_class = InternshipForm
    template_name = 'internships/internship_form.html'
    
    def test_func(self):
        internship = self.get_object()
        return (self.request.user.is_admin() or 
                (self.request.user.is_recruiter() and internship.recruiter == self.request.user))

@login_required
@student_required
def apply_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    
    # Check if the user has already applied
    existing_application = Application.objects.filter(
        internship=internship,
        student=request.user
    ).first()
    
    if existing_application:
        return HttpResponseForbidden("You have already applied to this internship.")
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.internship = internship
            application.student = request.user
            application.save()
            return redirect('internship-detail', pk=internship_id)
    else:
        form = ApplicationForm()
    
    return render(request, 'internships/apply_form.html', {
        'form': form,
        'internship': internship
    })