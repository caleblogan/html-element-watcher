from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic

from .models import WatchedElement


@login_required
def home(request):
    return render(request, 'watcher/home.html')


class WatchedElementDetailView(generic.DetailView):
    model = WatchedElement


class WatchedElementCreateView(generic.CreateView):
    model = WatchedElement
