from django.urls import path
from . import views

urlpatterns = [
    path('', views.InternshipListView.as_view(), name='internship-list'),
    path('<int:pk>/', views.InternshipDetailView.as_view(), name='internship-detail'),
    path('new/', views.InternshipCreateView.as_view(), name='internship-create'),
    path('<int:pk>/edit/', views.InternshipUpdateView.as_view(), name='internship-edit'),
    path('<int:internship_id>/apply/', views.apply_internship, name='internship-apply'),
]