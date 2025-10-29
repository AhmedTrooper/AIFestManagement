from django.db import models
from django.contrib.auth.models import User

class Role(models.TextChoices):
	AUTHORITY = "authority", "Authority"
	ADMIN = "admin", "Admin"
	JUDGE = "judge", "Judge"
	PARTICIPANT = "participant", "Participant"

class UserRole(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="role")
	role = models.CharField(max_length=32, choices=Role.choices, default=Role.PARTICIPANT)
	can_assign_admin = models.BooleanField(default=False)
	can_assign_judge = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.user.username}:{self.role}"

class Fest(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	starts_at = models.DateTimeField(null=True, blank=True)
	ends_at = models.DateTimeField(null=True, blank=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_fests")
	is_published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Item(models.Model):
	fest = models.ForeignKey(Fest, on_delete=models.CASCADE, related_name="items")
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	max_team_size = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f"{self.title} @ {self.fest.name}"

class ItemRule(models.Model):
	fest = models.ForeignKey(Fest, on_delete=models.CASCADE, related_name="rules")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="rules", null=True, blank=True)
	text = models.TextField()

	def __str__(self):
		return f"Rule for {self.item.title if self.item_id else self.fest.name}"

class Team(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="teams")
	name = models.CharField(max_length=200)
	members = models.ManyToManyField(User, related_name="teams", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} @ {self.item.title}"

class Submission(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
	link = models.URLField()
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Submission by {self.team.name}"
