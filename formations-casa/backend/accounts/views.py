from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import CoachProfile, TrainingCenterProfile
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CoachProfileSerializer,
    TrainingCenterProfileSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create", "register"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        """Get or update current user profile"""
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(
                request.user, data=request.data, partial=request.method == "PATCH"
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def coaches(self, request):
        """List all approved coaches"""
        coaches = User.objects.filter(role="coach", is_approved=True)
        serializer = self.get_serializer(coaches, many=True)
        return Response(serializer.data)


class CoachProfileViewSet(viewsets.ModelViewSet):
    queryset = CoachProfile.objects.all()
    serializer_class = CoachProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrainingCenterProfileViewSet(viewsets.ModelViewSet):
    queryset = TrainingCenterProfile.objects.all()
    serializer_class = TrainingCenterProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
