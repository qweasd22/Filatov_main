from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('visits/', views.VisitListView.as_view(), name='visit_list'),
    path('visits/<int:pk>/edit/', views.VisitUpdateView.as_view(), name='visit_edit'),
    path('visits/<int:pk>/delete/', views.VisitDeleteView.as_view(), name='visit_delete'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/create/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('doctors/<int:pk>/edit/', views.DoctorUpdateView.as_view(), name='doctor_edit'),
    path('doctors/<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
    path('logout/', views.logout_view, name='logout'),
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_edit'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    path('profile/', views.PatientProfileView.as_view(), name='patient_profile'),
    path('visits/create/', views.VisitCreateView.as_view(), name='visit_create'),
    path('visits/<int:pk>/', views.VisitDetailView.as_view(), name='visit_detail'),
    
]