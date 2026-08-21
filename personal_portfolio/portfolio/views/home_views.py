from django.shortcuts import render
from ..models import Project

def home(request):
    projects = Project.objects.filter(pinned=True).order_by("-id")[:2]
    return render(request, 'home.html', {'projects': projects})