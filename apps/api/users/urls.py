from django.urls import path
from .views import register, me

urlpatterns = [
	path("register/", register, name="register"),
	path("me/", me, name="me"),
]
