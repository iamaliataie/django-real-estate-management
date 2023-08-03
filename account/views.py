from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# Create your views here.

class Login(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy('property:home')