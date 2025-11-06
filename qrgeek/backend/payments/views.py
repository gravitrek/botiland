"""
Payment views for PayPal integration.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid

from accounts.models import SubscriptionPlan, UserSubscription
from .models import Payment


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout(request):
    """
    Create a PayPal checkout session.
    """
    plan_id = request.data.get('plan_id')
    billing_period = request.data.get('billing_period', 'monthly')

    try:
        plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
    except SubscriptionPlan.DoesNotExist:
        return Response(
            {'error': 'Plan not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Calculate amount
    amount = plan.price
    if billing_period == 'yearly':
        amount = plan.price * 12 * 0.8  # 20% discount for yearly

    # Create payment record
    payment = Payment.objects.create(
        user=request.user,
        amount=amount,
        payment_method='paypal',
        description=f'{plan.name} Plan - {billing_period}',
        metadata={
            'plan_id': str(plan.id),
            'billing_period': billing_period,
        },
        status='pending'
    )

    # For development: Return PayPal.me link
    # In production, you would integrate with PayPal REST API
    paypal_url = f"https://paypal.me/yagzud/{amount}"

    return Response({
        'payment_id': str(payment.id),
        'checkout_url': paypal_url,
        'amount': float(amount),
        'currency': 'USD',
        'description': payment.description,
        # Include a return URL for your app
        'return_url': f"{settings.FRONTEND_URL}/payment/success?payment_id={payment.id}",
        'cancel_url': f"{settings.FRONTEND_URL}/payment/cancelled",
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
    """
    Confirm payment completion and activate subscription.
    This would be called after PayPal payment confirmation.
    """
    payment_id = request.data.get('payment_id')
    paypal_order_id = request.data.get('paypal_order_id')

    try:
        payment = Payment.objects.get(
            id=payment_id,
            user=request.user,
            status='pending'
        )
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Update payment status
    payment.status = 'completed'
    payment.paypal_order_id = paypal_order_id
    payment.completed_at = timezone.now()
    payment.save()

    # Get plan details from payment metadata
    plan_id = payment.metadata.get('plan_id')
    billing_period = payment.metadata.get('billing_period', 'monthly')

    try:
        plan = SubscriptionPlan.objects.get(id=plan_id)
    except SubscriptionPlan.DoesNotExist:
        return Response(
            {'error': 'Plan not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Cancel existing active subscriptions
    UserSubscription.objects.filter(
        user=request.user,
        status='active'
    ).update(status='cancelled', cancelled_at=timezone.now())

    # Create new subscription
    starts_at = timezone.now()
    days = 30 if billing_period == 'monthly' else 365
    ends_at = starts_at + timedelta(days=days)

    subscription = UserSubscription.objects.create(
        user=request.user,
        plan=plan,
        status='active',
        starts_at=starts_at,
        ends_at=ends_at,
        payment_method='paypal'
    )

    # Link payment to subscription
    payment.subscription = subscription
    payment.save()

    # Update user's subscription plan
    request.user.subscription_plan = plan
    request.user.save()

    return Response({
        'message': 'Payment confirmed and subscription activated',
        'subscription_id': str(subscription.id),
        'plan_name': plan.name,
        'starts_at': starts_at,
        'ends_at': ends_at,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """Get user's payment history."""
    payments = Payment.objects.filter(user=request.user)

    payment_data = [{
        'id': str(payment.id),
        'amount': float(payment.amount),
        'currency': payment.currency,
        'description': payment.description,
        'status': payment.status,
        'created_at': payment.created_at,
        'completed_at': payment.completed_at,
    } for payment in payments]

    return Response(payment_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    """Cancel active subscription."""
    try:
        subscription = UserSubscription.objects.get(
            user=request.user,
            status='active'
        )
        subscription.status = 'cancelled'
        subscription.cancelled_at = timezone.now()
        subscription.save()

        return Response({
            'message': 'Subscription cancelled successfully',
            'ends_at': subscription.ends_at,
        })
    except UserSubscription.DoesNotExist:
        return Response(
            {'error': 'No active subscription found'},
            status=status.HTTP_404_NOT_FOUND
        )
