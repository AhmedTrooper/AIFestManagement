from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ["username", "email", "password"]

	def create(self, validated_data):
		user = User(username=validated_data["username"], email=validated_data.get("email", ""))
		user.set_password(validated_data["password"])
		user.save()
		return user
