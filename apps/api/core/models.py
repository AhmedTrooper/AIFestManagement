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
