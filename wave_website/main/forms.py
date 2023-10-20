from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Session, Transcript, SessionNote

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class PatientForm(forms.Form):
    full_name = forms.CharField(label="Full name", max_length=511)
    email = forms.EmailField(label="Email")
    contact = forms.CharField(label="Contact", max_length=24)
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Address",
        max_length=1000,
        required=False
    )
    education = forms.CharField(
        label="Highest education level attained",
        max_length=511,
        required=False
    )

    class Meta:
        model = Patient
        fields = ["full_name", "email", "contact", "emergency_contact", "address", "education"]


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ["session_date", "session_time", "patient"]
        widgets = {
            "session_date": forms.SelectDateWidget(),
            "session_time": forms.TimeInput(attrs={"type": "time"}),
        }


class SessionNotesForm(forms.ModelForm):
    client_history = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Client History", 
        required=False
    )
    repeated_lines = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Repeated Lines", 
        required=False
    )
    psychologists_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Psychologist's Notes", 
        required=False
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Summary",
        required=False
    )
    diagnosis = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Diagnosis",
        required=False
    )

    class Meta:
        model = SessionNote
        fields = ["client_history", "repeated_lines", "psychologists_notes", "summary", "diagnosis"]

class TranscriptForm(forms.ModelForm):
    text_file_url = forms.FileField(label="Upload Text Transcript", required=False)
    audio_file_url = forms.FileField(label="Upload Audio Recording", required=False)
    class Meta:
        model = Transcript
        fields = ["text_file_url", "audio_file_url"]
