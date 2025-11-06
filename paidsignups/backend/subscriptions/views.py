from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.utils import timezone
from .models import Subscription, Payment
from .serializers import (
    SubscriptionSerializer, SubscriptionCreateSerializer,
    PaymentSerializer, PaymentCreateSerializer
)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Subscription CRUD operations"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['plan', 'status']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Subscription.objects.all()
        return Subscription.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return SubscriptionCreateSerializer
        return SubscriptionSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a subscription"""
        subscription = self.get_object()
        subscription.status = 'CANCELLED'
        subscription.cancelled_at = timezone.now()
        subscription.cancellation_reason = request.data.get('reason', '')
        subscription.save()

        # Update user's subscription
        user = subscription.user
        user.subscription_active = False
        user.save()

        return Response({'detail': 'Subscription cancelled successfully.'})

    @action(detail=False, methods=['get'])
    def plans(self, request):
        """Get available subscription plans"""
        return Response(settings.SUBSCRIPTION_PLANS)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current user's active subscription"""
        subscription = Subscription.objects.filter(
            user=request.user,
            status='ACTIVE'
        ).first()

        if subscription:
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)

        return Response({
            'plan': 'FREE',
            'status': 'ACTIVE',
            'features': settings.SUBSCRIPTION_PLANS['FREE']
        })


class PaymentViewSet(viewsets.ModelViewSet):
    """Payment CRUD operations"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'payment_method']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer


class PayPalWebhookView(generics.GenericAPIView):
    """PayPal webhook handler"""
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """Handle PayPal webhook events"""
        event_type = request.data.get('event_type')
        resource = request.data.get('resource', {})

        # Handle different event types
        if event_type == 'PAYMENT.SALE.COMPLETED':
            # Handle successful payment
            pass
        elif event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
            # Handle subscription activation
            pass
        elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
            # Handle subscription cancellation
            pass

        return Response({'status': 'success'}, status=status.HTTP_200_OK)
