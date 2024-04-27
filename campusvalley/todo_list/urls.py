from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("signup", views.signup, name="singupPage"),
    path("loginform", views.loginForm, name="loginform"),
    path("signupform", views.signupForm, name="signupform"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("new_task", views.new_task, name="new_task"),
    path("logout", views.logout_user, name="logout")
]