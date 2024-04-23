from django.urls import path
from . import views
urlpatterns =[
    path("", views.password_generator, name="password_generator"),
]