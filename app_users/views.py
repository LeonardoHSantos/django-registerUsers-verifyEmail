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
        # incorrect_username_or_password
        # incorrect_forms
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            if not username or not password:
                context = {
                    "incorrect_forms": True,
                    "username": username,
                    "password": password
                }
                return render(request, "app/login.html", context=context)
            print(request.POST)
            print(username, password)

            get_users = User.objects.all()
            filter_user = User.objects.filter(username=username).first()
            print(f">>>>>> Total query: {filter_user}")
            if filter_user is None:
                context = {
                    "username": username,
                    "password": password,
                    "incorrect_username_or_password": True
                }
                return render(request, "app/login.html", context=context)
            
            profile_user = ProfileUser.objects.filter( user = filter_user).first()

            if not profile_user.is_verified:
                context = {
                    "username": username,
                    "password": password,
                    "account_not_validated": True
                }
                return render(request, "app/login.html", context=context)

            user = authenticate(username=username, password=password)
            if user is None:
                context = {
                    "username": username,
                    "password": password,
                    "incorrect_username_or_password": True
                }
                return render(request, "app/login.html", context=context)
            auth_login(request, user)
            print(">>>>>> Usuário autenticado com sucesso...")

        except Exception as e:
            print(e)
            return render(request, "app/login.html")

def logout_user(request):
    logout(request)
    return redirect("/login/")

def register(request):
    if request.method == "GET":
        return render(request, "app/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(request.POST)
        print(username, email, password)

        if User.objects.filter(username=username).first():
            print("Este usuário já existe.")
            context = {
                "username": username,
                "email": email,
                "password": password,
                "username_already_exists": True
            }
            return render(request, "app/register.html", context=context)
        elif User.objects.filter(email=email).first():
            print("Este email já existe.")
            context = {
                "username": username,
                "email": email,
                "password": password,
                "email_already_exists": True
            }
            return render(request, "app/register.html", context=context)
        
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        auth_token = str(uuid.uuid4())
        profile_user = ProfileUser.objects.create(user=user_obj, auth_token=auth_token)
        profile_user.save()

        # context = {
        #     "username": username,
        #     "email": email,
        #     "password": password,
        #     "username_already_exists": False,
        #     "email_already_exists": True
        # }
        return render(request, "app/register.html", context=context) 

def send_mail_validated_account(username, email, token):
    pass
