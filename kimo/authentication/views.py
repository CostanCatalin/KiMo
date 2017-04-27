from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserLoginForm, RegistrationForm
from .models import Account
# Create your views here.


def login_view(request):
    return render(request, "authentication/login_page.html")


def register_view(request):
    return render(request, "authentication/register_page.html")


def logout_view(request):
    return redirect("/account/login/")


def profile(request):
    return render(request, 'authentication/profile.html')

