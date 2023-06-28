# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
