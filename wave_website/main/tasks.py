from .models import Patient
from celery import shared_task

@shared_task
def count_patients():
    print(f'# of patients: {Patient.objects.count()}')
