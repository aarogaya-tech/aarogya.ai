from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('clients', views.clients, name='clients'),
    path('new-client', views.new_client, name='new-client'),
    path('client/<int:client_id>', views.client_detail, name='client-detail'),
    path('new-session', views.new_client_session, name='new-client-session')
]
