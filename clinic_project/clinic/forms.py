from django import forms
from .models import Visit, Doctor, Patient, Service

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['doctor', 'date', 'diagnosis', 'services']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'services': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'user':
            self.fields['patient'] = forms.ModelChoiceField(
                queryset=Patient.objects.filter(user=user),
                widget=forms.HiddenInput(),
                initial=user.patient_profile
            )

from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'specialty': forms.Select(choices=Doctor.SPECIALTY_CHOICES),
            'category': forms.Select(choices=Doctor.CATEGORY_CHOICES),
        }

from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'birth_year': forms.NumberInput(attrs={
                'min': 1900, 
                'max': 2100,
                'class': 'form-control'
            }),
            'discount_category': forms.Select(attrs={'class': 'form-select'}),
        }
        exclude = ['created_by', 'created_at']


from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'cost': forms.NumberInput(attrs={'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }