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
            return redirect("/painel/")
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

        if not username or not email or not password:
                context = {
                    "incorrect_forms": True,
                    "username": username,
                    "email": email,
                    "password": password,
                }
                return render(request, "app/register.html", context=context)

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

        context = {
            "mensagem_check_email_token": True
        }
        send_mail_validated_account(username=username, email=email, token=auth_token)
        return render(request, "app/register.html", context=context) 

def send_mail_validated_account(username, email, token):
    subject = 'Verifique sua conta'
    message = f'Olá {username}, valide sua conta acessando este link http://127.0.0.1:8000/verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(subject)
    print(message)
    print(from_email)
    print(recipient_list)
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=f"""
        <p>Sua conta está a um clique de você.</p>
        <p>{message}</p>
        """)

def varify_account_user(request, auth_token):
    try:
        profile_auth = ProfileUser.objects.filter(auth_token=auth_token).first()
        if profile_auth:
            if profile_auth.is_verified:
                context = {
                    "already_verified_account": True
                }
                return render(request, "app/page_success_account.html", context=context)
            profile_auth.is_verified = True
            profile_auth.save()
            context = {
                "successfully_verified_account": True
            }
            return render(request, "app/page_success_account.html", context=context)
        else:
            return redirect("/error-verify-accounts/")
    except Exception as e:
        print(e)
        return redirect("/error-verify-accounts/")

def error_verify_accounts (request):
    return render(request, "app/error_verify_accounts.html")

def painel_user(request):
    return render(request, "painel_user/painel.html")

