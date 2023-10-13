from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Session, Transcript
from django.forms import inlineformset_factory


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
    emergency_contact = forms.CharField(label="Emergency Contact", max_length=24)

    class Meta:
        model = Patient
        fields = ["full_name", "email", "contact", "emergency_contact"]


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ["session_date", "session_time", "patient"]
        widgets = {
            "session_date": forms.SelectDateWidget(),
            "session_time": forms.TimeInput(attrs={"type": "time"}),
        }


class TranscriptForm(forms.ModelForm):
    class Meta:
        model = Transcript
        fields = ["text_file_url"]
