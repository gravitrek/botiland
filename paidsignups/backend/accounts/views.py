from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserRegistrationSerializer, ChangePasswordSerializer

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """Change password endpoint"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User viewset for admin"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['subscription_plan', 'subscription_active', 'is_verified']
    search_fields = ['username', 'email', 'company_name']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user statistics"""
        user = request.user
        return Response({
            'subscription_plan': user.subscription_plan,
            'subscription_active': user.subscription_active,
            'forms_created': user.forms_created,
            'landing_pages_created': user.landing_pages_created,
            'leads_this_month': user.leads_this_month,
            'total_leads': user.leads.count(),
            'total_forms': user.forms.count(),
            'total_landing_pages': user.landing_pages.count(),
        })
