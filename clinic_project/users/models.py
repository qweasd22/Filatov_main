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
    birth_year = models.IntegerField('Год рождения')