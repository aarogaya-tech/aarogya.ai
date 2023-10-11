from django.contrib import admin

from .models import Patient, Session, Transcript

admin.site.register(Patient)
admin.site.register(Session)
admin.site.register(Transcript)
