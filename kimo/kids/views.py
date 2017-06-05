from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Kid
from .forms import RegisterKidForm


def list_kids(request):
    return render(request, 'kids/list_kids.html')


def register_kid(request):
    return render(request, 'kids/form.html', {'form': form})


def edit_kid(request, kid_id):
    return render(request, 'kids/form.html', {'form': form})


def view_kid(request, kid_id):
    return render(request, 'kids/view.html')


def delete_kid(request, kid_id):
    return redirect('/kids/list')
