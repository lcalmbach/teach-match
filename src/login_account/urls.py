from django.urls import path
from django.contrib.auth import views
from . import views

app_name = "login_account"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.user_profile, name="profile"),
]
