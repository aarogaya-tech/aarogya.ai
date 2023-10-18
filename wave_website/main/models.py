from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    full_name = models.CharField(max_length=511)
    email = models.EmailField()
    contact = models.CharField(max_length=24)
    address = models.CharField(max_length=1000, null=True)
    education = models.CharField(max_length=511, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __to_dict__(self):
        return {'full_name': self.full_name, 'id': self.id}

    def __str__(self):
        return self.full_name

class Session(models.Model):
    session_date = models.DateField()
    session_time = models.TimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SessionNote(models.Model):
    repeated_lines = models.CharField(max_length=1000)
    psychologists_notes = models.CharField(max_length=1000)
    summary = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


def transcript_file_upload(instance, filename):
    ext = filename.rsplit('.', 1)[-1]
    filename = f'Patient-{instance.session.patient.id}\
        -Session-{instance.session.session_date.strftime("%Y%m%d")}\
        -{instance.session.session_time.strftime("%H%M")}-Transcript'

    full_upload_path = f"transcripts/{filename}.{ext}"
    return full_upload_path


class Transcript(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    text_file_url = models.FileField(upload_to=transcript_file_upload, null=True)
    audio_file_url = models.FileField(upload_to=transcript_file_upload, null=True)
    generated_transcript = models.FileField(upload_to=transcript_file_upload, null=True)
    transcript_generation_in_progress = models.BooleanField(default=True)
