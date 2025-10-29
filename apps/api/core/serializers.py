from rest_framework import serializers
from .models import Fest, UserRole

class FestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fest
		fields = ["id", "name", "description", "starts_at", "ends_at", "is_published", "created_at", "updated_at"]

class UserRoleSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source="user.username", read_only=True)
	class Meta:
		model = UserRole
		fields = ["username", "role", "can_assign_admin", "can_assign_judge"]
