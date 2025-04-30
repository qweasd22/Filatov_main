# clinic/views.py
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Visit, VisitService
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Doctor, Visit
from .forms import VisitForm, DoctorForm
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from users.decorators import role_required
from .models import Doctor
from .forms import DoctorForm
from django.contrib import messages

@login_required
@user_passes_test(lambda u: u.role in ["admin", "user"])
def visit_list(request):
    visits = Visit.objects.all()
    return render(request, "clinic/visit_list.html", {"visits": visits})



@method_decorator(role_required(['user', 'admin']), name='dispatch')
class VisitListView(ListView):
    template_name = 'clinic/visit_list.html'
    context_object_name = 'visits'
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Visit.objects.all()
        return Visit.objects.filter(created_by=self.request.user)

# Для всех аутентифицированных
@method_decorator(role_required(['user', 'admin']), name='dispatch')
class VisitCreateView(CreateView):
    model = Visit
    form_class = VisitForm
    template_name = 'clinic/visit_form.html'
    success_url = reverse_lazy('visit_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# Только для админов
@method_decorator(role_required(['admin']), name='dispatch')
class VisitUpdateView(UpdateView):
    model = Visit
    form_class = VisitForm
    template_name = 'clinic/visit_form.html'
    success_url = reverse_lazy('visit_list')

@method_decorator(role_required(['admin']), name='dispatch')
class VisitDeleteView(DeleteView):
    model = Visit
    template_name = 'clinic/visit_confirm_delete.html'
    success_url = reverse_lazy('visit_list')

def logout_view(request):
    logout(request)
    return redirect('login')

from users.decorators import role_required

@role_required(['admin'])
def admin_dashboard(request):
    # Логика для администратора
    return render(request, "clinic/admin_dashboard.html")

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from users.decorators import role_required
from .models import Patient
from .forms import PatientForm
from django.utils.decorators import method_decorator

@method_decorator(role_required(['admin']), name='dispatch')
class PatientListView(ListView):
    model = Patient
    template_name = 'clinic/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 15
    ordering = ['-created_at']

@method_decorator(role_required(['admin']), name='dispatch')
class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'clinic/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@method_decorator(role_required(['admin']), name='dispatch')
class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'clinic/patient_form.html'
    success_url = reverse_lazy('patient_list')

@method_decorator(role_required(['admin']), name='dispatch')
class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'clinic/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')
    
class DoctorListView(ListView):
    model = Doctor
    template_name = 'clinic/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 10

# Только для админов
@method_decorator(role_required(['admin']), name='dispatch')
class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'clinic/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

@method_decorator(role_required(['admin']), name='dispatch')
class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'clinic/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

@method_decorator(role_required(['admin']), name='dispatch')
class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'clinic/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')

def home_view(request):
    return render(request, "home.html")

from .models import Service
from .forms import ServiceForm
class ServiceListView(ListView):
    model = Service
    template_name = 'clinic/service_list.html'
    context_object_name = 'services'
    ordering = ['name']

# Только для администраторов
@method_decorator(role_required(['admin']), name='dispatch')
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'clinic/service_form.html'
    success_url = reverse_lazy('service_list')

@method_decorator(role_required(['admin']), name='dispatch')
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'clinic/service_form.html'
    success_url = reverse_lazy('service_list')

@method_decorator(role_required(['admin']), name='dispatch')
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'clinic/service_confirm_delete.html'
    success_url = reverse_lazy('service_list')
from django.views.generic import DetailView
# Профиль пациента
@method_decorator(login_required, name='dispatch')
class PatientProfileView(UpdateView):
    model = Patient
    form_class = PatientForm  # Создайте форму для Patient
    template_name = 'clinic/patient_profile.html'
    success_url = reverse_lazy('visit_list')

    def get_object(self):
        return self.request.user.patient

# Детали визита
@method_decorator(login_required, name='dispatch')
class VisitDetailView(DetailView):
    model = Visit
    template_name = 'clinic/visit_detail.html'
    context_object_name = 'visit'

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Visit.objects.all()
        return Visit.objects.filter(created_by=self.request.user)
    
# clinic/views.py
class VisitCreateView(CreateView):
    model = Visit
    form_class = VisitForm
    template_name = 'clinic/visit_form.html'
    success_url = reverse_lazy('visit_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Автоматическая привязка пациента и создателя
        if self.request.user.role == 'user':
            form.instance.patient = self.request.user.patient_profile
        form.instance.created_by = self.request.user
        
        # Сохраняем обращение
        response = super().form_valid(form)
        
        # Создаем связи с услугами
        for service in form.cleaned_data['services']:
            VisitService.objects.create(
                visit=self.object,
                service=service,
                quantity=1
            )
        
        # Обновляем стоимость
        self.object.save()
        return response
class VisitListView(ListView):
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Visit.objects.all()
        return Visit.objects.filter(created_by=self.request.user)