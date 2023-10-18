from datetime import datetime
from django.shortcuts import render, redirect
from .forms import RegisterForm, PatientForm, SessionForm, SessionNotesForm, TranscriptForm
from .models import Patient, Session, SessionNote
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.models import User
# Create your views here.


@login_required()
def home(request):
    all_clients = Patient.objects.filter(user=request.user)
    all_sessions = Session.objects.filter(user=request.user)
    today = []
    upcoming = []
    past = []

    for session in all_sessions:
        if session.session_date == datetime.today().date():
            today.append({
                "session_date": session.session_date,
                "session_time": session.session_time,
                "client_name": session.patient,
                "client_id": session.__dict__['patient_id'],
                "session_id": session.__dict__['id'],
            })
        elif session.session_date > datetime.today().date():
            upcoming.append({
                "session_date": session.session_date,
                "session_time": session.session_time,
                "client_name": session.patient,
                "client_id": session.__dict__['patient_id'],
                "session_id": session.__dict__['id'],
            })
        else:
            past.append({
                "session_date": session.session_date,
                "session_time": session.session_time,
                "client_name": session.patient,
                "client_id": session.__dict__['patient_id'],
                "session_id": session.__dict__['id'],
            })

    return render(
        request,
        "main/home.html", 
        {
            "clients": all_clients, 
            "today_sessions": today,
            "upcoming_sessions": upcoming,
            "past_sessions": past 
        }
    )


@login_required()
def clients(request):
    all_clients = Patient.objects.all()
    logged_in_user = User.objects.get(username=request.user)
    clients = [
        {
            "id": client.id, 
            "full_name": client.full_name
        } for client in all_clients if client.user == logged_in_user
    ]

    return render(request, "main/clients.html", {"all_clients": clients})


@login_required
def client_detail(request, client_id: int, session_id=None):
    if request.method == "POST":
        session_notes_form = SessionNotesForm(request.POST)
        if session_notes_form.is_valid():
            SessionNote.objects.create(
                **session_notes_form.cleaned_data, 
                **{
                    "session": Session.objects.get(id=session_id),
                    "user": request.user
                }
            )
            return redirect(
                reverse("client-detail-with-transcript", kwargs={"client_id": client_id, "session_id": session_id})
            )

    try:
        client = Patient.objects.get(pk=client_id)
        logged_in_user = User.objects.get(username=request.user)
        if client.user.username != logged_in_user.username:
            raise Exception("User not authorized to access client")

        sessions = client.session_set.all()
        transcript = None
        session_notes_form = SessionNotesForm()
        session = None
        note = None
        if session_id is not None:
            session = Session.objects.get(id=session_id)
            try:
                note = None if SessionNote.objects.count() == 0 \
                    else SessionNote.objects.get(session=session)
            except SessionNote.DoesNotExist:
                note = None

            if note:
                session_notes_form = SessionNotesForm(instance=note)

            if session.id == session_id:
                if session.user.username != logged_in_user.username:
                    raise Exception("User not authorized to access session")
                transcript = session.transcript_set.all()[0]
                try:
                    transcript.content = transcript.text_file_url.file.read().decode('utf-8')
                except ValueError:
                    transcript = None

    except Patient.DoesNotExist:
        raise Http404("Patient does not exist.")

    return render(
        request,
        "main/client_detail.html", 
        {
            "client": client,
            "sessions": sessions,
            "transcript": transcript,
            "session": session,
            "session_notes": session_notes_form,
            "notes": note
        }
    )


@login_required
def new_client_session(request, client_id: int):
    if request.method == "POST":
        session_form = SessionForm(request.POST)
        transcript_form = TranscriptForm(request.POST, request.FILES)
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
        session_form.fields["patient"].queryset = Patient.objects.filter(id=client_id)
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
        user = User.objects.get(username=request.user)
        if not user:
            return {'message':'Hmm.. this shouldn\'t happen'}
        if form.is_valid():
            Patient.objects.create(**form.cleaned_data, **{'user': user})
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
