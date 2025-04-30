from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Администратор'),
        ('user', 'Пользователь')
    )
    role = models.CharField(
        'Роль', 
        max_length=20, 
        choices=ROLES, 
        default='user'
    )
    patient = models.OneToOneField(
        'clinic.Patient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_user"  # Уникальное related_name
    )