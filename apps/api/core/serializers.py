from rest_framework import serializers
from .models import Fest, UserRole, Item, ItemRule

class ItemRuleSerializer(serializers.ModelSerializer):
	class Meta:
		model = ItemRule
		fields = ["id", "text", "item"]

class ItemSerializer(serializers.ModelSerializer):
	rules = ItemRuleSerializer(many=True, read_only=True)
	class Meta:
		model = Item
		fields = ["id", "title", "description", "max_team_size", "rules"]

class FestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fest
		fields = ["id", "name", "description", "starts_at", "ends_at", "is_published", "created_at", "updated_at"]

class FestCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fest
		fields = ["name", "description", "starts_at", "ends_at", "is_published"]

	def create(self, validated_data):
		user = self.context["request"].user
		return Fest.objects.create(created_by=user, **validated_data)

class FestDetailSerializer(FestSerializer):
	items = ItemSerializer(many=True, read_only=True)
	rules = ItemRuleSerializer(many=True, read_only=True)
	class Meta(FestSerializer.Meta):
		fields = FestSerializer.Meta.fields + ["items", "rules"]

class UserRoleSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source="user.username", read_only=True)
	class Meta:
		model = UserRole
		fields = ["username", "role", "can_assign_admin", "can_assign_judge"]
