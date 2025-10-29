from rest_framework.permissions import BasePermission
from .models import UserRole, Role

class IsAuthority(BasePermission):
	def has_permission(self, request, view):
		if not request.user or not request.user.is_authenticated:
			return False
		try:
			user_role = UserRole.objects.get(user=request.user)
			return user_role.role == Role.AUTHORITY
		except UserRole.DoesNotExist:
			return False
