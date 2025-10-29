from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from core.models import UserRole, Role

@api_view(["POST"]) 
@permission_classes([AllowAny])
def register(request):
	serializer = RegisterSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response({"detail": "registered"}, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"]) 
@permission_classes([IsAuthenticated])
def me(request):
	try:
		ur = UserRole.objects.get(user=request.user)
		role = ur.role
	except UserRole.DoesNotExist:
		role = Role.PARTICIPANT
	return Response({"username": request.user.username, "role": role})
