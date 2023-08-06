from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm

# Create your views here.

class Login(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy('property:home')
    

class Register(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')