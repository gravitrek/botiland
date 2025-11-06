"""
Views for user authentication and management.
"""
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

from .models import User, SubscriptionPlan, UserSubscription
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    SubscriptionPlanSerializer,
    UserSubscriptionSerializer,
    PasswordChangeSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    POST /api/auth/register/
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Registration successful. Please verify your email.'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    User login endpoint.
    POST /api/auth/login/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Update last login
        user.last_login_at = timezone.now()
        user.save(update_fields=['last_login_at'])

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile.
    GET/PUT /api/auth/profile/
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """
    Change user password.
    POST /api/auth/password/change/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, user)

        return Response({
            'message': 'Password changed successfully.'
        })


class SubscriptionPlanListView(generics.ListAPIView):
    """
    List all available subscription plans.
    GET /api/auth/plans/
    """
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]


class UserSubscriptionView(generics.RetrieveAPIView):
    """
    Get user's current subscription.
    GET /api/auth/subscription/
    """
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserSubscription.objects.filter(
            user=self.request.user,
            status='active'
        ).first()


class SubscriptionUpgradeView(APIView):
    """
    Upgrade user subscription.
    POST /api/auth/subscription/upgrade/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')

        if not plan_id:
            return Response(
                {'error': 'plan_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            return Response(
                {'error': 'Plan not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # TODO: Implement payment processing logic here
        # For now, just create the subscription

        # Cancel existing active subscriptions
        UserSubscription.objects.filter(
            user=request.user,
            status='active'
        ).update(status='cancelled', cancelled_at=timezone.now())

        # Create new subscription
        from datetime import timedelta
        starts_at = timezone.now()
        ends_at = starts_at + timedelta(days=30 if plan.billing_period == 'monthly' else 365)

        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            status='active',
            starts_at=starts_at,
            ends_at=ends_at,
        )

        # Update user's subscription plan
        request.user.subscription_plan = plan
        request.user.save()

        return Response({
            'message': 'Subscription upgraded successfully',
            'subscription': UserSubscriptionSerializer(subscription).data
        })


class DeleteAccountView(APIView):
    """
    Delete user account.
    DELETE /api/auth/account/
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        return Response({
            'message': 'Account deactivated successfully'
        }, status=status.HTTP_204_NO_CONTENT)
