from django.db import models
from users.models import CustomUser
from billing.models import Discount
from django.db.models import Sum,F

class Doctor(models.Model):
    SPECIALTY_CHOICES = [("терапевт", "Терапевт"), ("хирург", "Хирург")]  # и другие
    CATEGORY_CHOICES = [("первая", "Первая"), ("высшая", "Высшая")]
    
    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100)
    specialty = models.CharField("Специальность", max_length=50, choices=SPECIALTY_CHOICES)
    category = models.CharField("Категория", max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )
    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    birth_year = models.IntegerField("Год рождения")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Visit(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField("Дата обращения")
    diagnosis = models.TextField("Диагноз")
    services = models.ManyToManyField('Service', through='VisitService')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    total_cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, default=0)

    def calculate_total_cost(self):
        total = self.visitservice_set.aggregate(
            total=Sum(F('service__cost') * F('quantity'))
        )['total'] or 0
        return total

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)

class VisitService(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Service(models.Model):
    name = models.CharField("Название услуги", max_length=200, unique=True)
    cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.cost} руб."

