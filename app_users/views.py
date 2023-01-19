from django.shortcuts import render

def home(request):
    return render(request, "app/home.html")
def login(request):
    return render(request, "app/login.html")
def logout(request):
    print("Logout da sessão")
    return render(request, "app/login.html")
def register(request):
    return render(request, "app/register.html")