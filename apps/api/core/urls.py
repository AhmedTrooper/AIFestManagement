from django.urls import path
from .views import echo

urlpatterns = [
    path("echo", echo, name="echo"),
]
