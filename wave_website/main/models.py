from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    full_name = models.CharField(max_length=511)
    email = models.EmailField()
    contact = models.CharField(max_length=24)
    emergency_contact = models.CharField(max_length=24)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __to_dict__(self):
        return {'full_name': self.full_name, 'id': self.id}

    # def __str__(self):
    #     return self.full_name

class Session(models.Model):
    session_date = models.DateField()
    session_time = models.TimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Transcript(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    audio_file_url = models.CharField(max_length=255)
    text_file_url = models.CharField(max_length=255)
