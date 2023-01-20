from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name="register"),
    path("verify/<auth_token>", views.varify_account_user, name="verify"),
    path("error-verify-accounts/", views.error_verify_accounts, name="error_verify_accounts"),
    path("painel/", views.painel_user, name="painel"),
]