from django.urls import path
from .views import echo, fest_list, fest_create

urlpatterns = [
	path("echo", echo, name="echo"),
	path("fests", fest_list, name="fest_list"),
	path("fests/create", fest_create, name="fest_create"),
]
