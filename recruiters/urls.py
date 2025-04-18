from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecruiterListView.as_view(), name='recruiter-list'),
    path('<int:pk>/', views.RecruiterDetailView.as_view(), name='recruiter-detail'),
    path('<int:pk>/edit/', views.RecruiterUpdateView.as_view(), name='recruiter-edit'),
]