from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def home(request):
    context = {
        'posts': Question.objects.all()
    }
    return render(request, 'forum/home.html', context)

def about(request):
    return render(request, 'forum/about.html', {'title': 'About'})
