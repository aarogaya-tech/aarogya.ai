from django.shortcuts import render, redirect
from .forms import RegisterForm, PatientForm
from .models import Patient
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

@login_required()
def home(request):
    return render(request, 'main/home.html')

@login_required()
def clients(request):
    all_clients = Patient.objects.all()
    logged_in_user = User.objects.get(username=request.user)
    clients = [
        {
            'id': client.id, 
            'full_name': client.full_name
        } for client in all_clients if client.user == logged_in_user
    ]

    return render(request, 'main/clients.html', {'all_clients': clients})

@login_required()
def new_client(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        user = User.objects.get(username=request.user)
        if not user:
            return {'message':'Hmm.. this shouldn\'t happen'}
        if form.is_valid():
            Patient.objects.create(**form.cleaned_data, **{'user': user})
            return redirect('/clients')
    else:
        form = PatientForm()

    return render(request, 'forms/add_client.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {'form': form})
