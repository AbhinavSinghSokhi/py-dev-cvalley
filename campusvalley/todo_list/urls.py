from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("signup", views.signup, name="singupPage"),
    path("loginform", views.loginForm, name="loginform"),
    path("signupform", views.signupForm, name="signupform"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("new_task", views.new_task, name="new_task"),
    path("logout", views.logout_user, name="logout"),
    path("delete_task", views.delete_task, name="delete_task"),
    path("mark_completed", views.mark_completed, name="mark_completed"),
    path("upcoming_tasks",views.upcoming_tasks, name="upcoming_tasks"),
    path("completed_tasks", views.completed_tasks, name="completed_tasks"),
    path("personal_tasks", views.personal_tasks, name="personal_tasks"),
    path("home_tasks", views.home_tasks, name="home_tasks"),
    path("work_tasks", views.work_tasks, name="work_tasks"),
]