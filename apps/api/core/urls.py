from django.urls import path
from .views import echo, fest_list

urlpatterns = [
	path("echo", echo, name="echo"),
	path("fests", fest_list, name="fest_list"),
]
