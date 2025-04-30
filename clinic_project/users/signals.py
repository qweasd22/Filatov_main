from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from clinic.models import Patient

@receiver(post_save, sender=CustomUser)
def create_patient(sender, instance, created, **kwargs):
    if created and instance.role == 'user':
        Patient.objects.create(user=instance)