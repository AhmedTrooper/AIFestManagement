from django.urls import path
from .views import echo, fest_list, fest_create, fest_detail, fest_ask, item_ask

urlpatterns = [
	path("echo", echo, name="echo"),
	path("fests", fest_list, name="fest_list"),
	path("fests/create", fest_create, name="fest_create"),
	path("fests/<int:fest_id>", fest_detail, name="fest_detail"),
	path("fests/<int:fest_id>/ask", fest_ask, name="fest_ask"),
	path("items/<int:item_id>/ask", item_ask, name="item_ask"),
]
