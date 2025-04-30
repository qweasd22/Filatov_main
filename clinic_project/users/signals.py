from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from clinic.models import Patient

@receiver(post_save, sender=CustomUser)
def create_patient(sender, instance, created, **kwargs):
    if created and instance.role == 'user':
        Patient.objects.create(
            user=instance,
            last_name=instance.last_name,
            first_name=instance.first_name,
            middle_name=getattr(instance, 'middle_name', ''),
            birth_year=instance.birth_year  # Используем значение из формы
        )