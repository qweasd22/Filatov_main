from django.contrib import admin
from .models import Visit, Doctor, Patient, Service


admin.site.register(Visit)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Service)
