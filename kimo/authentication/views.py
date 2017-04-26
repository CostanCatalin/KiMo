from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserLoginForm, RegistrationForm
from .models import Account
# Create your views here.


def login_view(request):
    """
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/account/profile")
    """
    return render(request, "authentication/login_page.html")


def register_view(request):
    """
    title = 'Register'
    form = RegistrationForm(request.POST or None)
    context = {
        'form': form,
        'title': title
    }
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        return redirect("/account/login/")
    """
    return render(request, "authentication/register_page.html")


def logout_view(request):
    # logout(request)
    return redirect("/account/login/")


# @login_required()
def profile(request):
    return render(request, 'authentication/profile.html')

"""
def list_users(request):
    users_list = Account.objects.all()
    paginator = Paginator(users_list, 25)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'authentication/list_users.html', {'users': users})
"""

