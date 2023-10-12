from django.shortcuts import render, redirect
from .forms import RegisterForm, PatientForm, SessionForm, TranscriptForm
from .models import Patient
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse

# Create your views here.


@login_required()
def home(request):
    return render(request, "main/home.html")


@login_required()
def clients(request):
    all_clients = Patient.objects.all()
    clients = [
        {"id": client.id, "full_name": client.full_name} for client in all_clients
    ]

    return render(request, "main/clients.html", {"all_clients": clients})


@login_required
def client_detail(request, client_id: int):
    try:
        client = Patient.objects.get(pk=client_id)
        sessions = client.session_set.all()
        for session in sessions:
            session.transcripts = session.transcript_set.all()
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist.")

    return render(request, "main/client_detail.html", {"client": client, 'sessions': sessions})


@login_required
def new_client_session(request):
    if request.method == "POST":
        session_form = SessionForm(request.POST)
        transcript_form = TranscriptForm(request.POST)
        if session_form.is_valid() and transcript_form.is_valid():
            session_form.instance.user = request.user
            client_session = session_form.save(commit=False)
            client_session.save()
            transcript_form.instance.session = client_session
            transcript_form.save()
            return redirect(
                reverse("client-detail", kwargs={"client_id": client_session.patient.id})
            )
    else:
        session_form = SessionForm()
        transcript_form = TranscriptForm()
        return render(
            request,
            "forms/add_session.html",
            {
                "session_form": session_form,
                "transcript_form": transcript_form,
            },
        )


@login_required()
def new_client(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            Patient.objects.create(**form.cleaned_data)
            return redirect("/clients")
    else:
        form = PatientForm()

    return render(request, "forms/add_client.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})
