from django.contrib import admin
from django.urls import path, include

from projectManagementPortalApp import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("forget_password/", views.forget_password, name="forget_password"),
    path("dashboard/", views.dashboard, name="dashboard"),
]