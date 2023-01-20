import uuid
from django.shortcuts import render, redirect

from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login

from .models import ProfileUser




def home(request):
    return render(request, "app/home.html")
def login(request):
    if request.method == "GET":
        return render(request, "app/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(request.POST)
        print(username, password)
        context = {
            "username": username,
            "password": password
        }
        return render(request, "app/login.html", context=context)

def register(request):
    if request.method == "GET":
        return render(request, "app/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(request.POST)
        print(username, email, password)
        context = {
            "username": username,
            "email": email,
            "password": password,
            "username_already_exists": False,
            "email_already_exists": True
        }
        return render(request, "app/register.html", context=context) 


def logout(request):
    print("Logout da sessão")
    return render(request, "app/login.html")