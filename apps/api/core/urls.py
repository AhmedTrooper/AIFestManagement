from django.urls import path
from .views import echo, fest_list, fest_create, fest_detail, fest_ask, item_ask, fest_item_create, item_rule_create, fest_rule_create, item_teams, team_submission_create

urlpatterns = [
	path("echo", echo, name="echo"),
	path("fests", fest_list, name="fest_list"),
	path("fests/create", fest_create, name="fest_create"),
	path("fests/<int:fest_id>", fest_detail, name="fest_detail"),
	path("fests/<int:fest_id>/ask", fest_ask, name="fest_ask"),
	path("items/<int:item_id>/ask", item_ask, name="item_ask"),
	path("fests/<int:fest_id>/items", fest_item_create, name="fest_item_create"),
	path("items/<int:item_id>/rules", item_rule_create, name="item_rule_create"),
	path("fests/<int:fest_id>/rules", fest_rule_create, name="fest_rule_create"),
	path("items/<int:item_id>/teams", item_teams, name="item_teams"),
	path("teams/<int:team_id>/submissions", team_submission_create, name="team_submission_create"),
]
