from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.urls import reverse


from ..boards.models import Board


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            boards = Board.objects.all().order_by('-created_at')
            return render(request, 'boards/home.html', {'boards': boards})

    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

from django.shortcuts import render

