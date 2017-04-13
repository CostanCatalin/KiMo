from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Kids
from .forms import RegisterKidForm


@login_required()
def list_kids(request):
    kids_query = Kids.objects.of_user(request.user.pk)
    context = {
        'kids': kids_query
    }
    return render(request, 'kids/list_kids.html', context)


@login_required()
def register_kid(request):
    form = RegisterKidForm(request.POST or None)

    if form.is_valid():
        kid = form.save(commit=False)
        kid.parent = request.user
        kid.last_name = request.user.last_name
        kid.save()
        return redirect('/kids/list')

    return render(request, 'kids/form.html', {'form': form})


def edit_kid(request, kid_id):
    if request.method == 'POST':
        kid_qr = get_object_or_404(Kids, pk=kid_id)
        form = RegisterKidForm(request.POST, instance=kid_qr)
        if form.is_valid():
            kid = form.save(commit=False)
            kid.parent = request.user
            kid.last_name = request.user.last_name
            kid.save()
            return redirect('/kids/list')
    else:
        kid = get_object_or_404(Kids, pk=kid_id)
        form = RegisterKidForm(instance=kid)

    return render(request, 'kids/form.html', {'form': form})


@login_required()
def view_kid(request, kid_id):
    kid_qr = get_object_or_404(Kids, pk=kid_id)
    if kid_qr.parent != request.user:
        return HttpResponseForbidden()
    return render(request, 'kids/view.html', {'kid': kid_qr, 'age': kid_qr.get_age()})


@login_required()
def delete_kid(request, kid_id):
    kid_qr = get_object_or_404(Kids, pk=kid_id)
    if kid_qr.parent != request.user:
        return HttpResponseForbidden()
    kid_qr.delete()
    return redirect('/kids/list')

def list_stats(request):
    percentages = []
    months = []
    for i in range(1, 20):
        stat = Kids.objects.stats(i)
        if stat and stat > 0.0:
            percentages.append((i, stat))
    for i in range(1, 13):
        months.append((i, Kids.objects.registered_in_month(i)))

    return render(request, 'kids/stats.html', {'percentages': percentages, 'months': months})
