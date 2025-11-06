from rest_framework import serializers
from .models import Subscription, Payment


class SubscriptionSerializer(serializers.ModelSerializer):
    """Subscription serializer"""

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'user', 'user_email', 'plan', 'amount',
            'paypal_subscription_id', 'paypal_order_id',
            'paypal_payer_id', 'paypal_payer_email',
            'status', 'start_date', 'end_date', 'next_billing_date',
            'cancelled_at', 'cancellation_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Subscription creation serializer"""

    class Meta:
        model = Subscription
        fields = [
            'plan', 'amount', 'paypal_subscription_id', 'paypal_order_id',
            'paypal_payer_id', 'paypal_payer_email',
            'status', 'start_date', 'end_date', 'next_billing_date'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return Subscription.objects.create(user=user, **validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer"""

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'subscription', 'user', 'user_email',
            'amount', 'currency',
            'paypal_payment_id', 'paypal_payer_id', 'paypal_payer_email',
            'status', 'payment_method', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Payment creation serializer"""

    class Meta:
        model = Payment
        fields = [
            'subscription', 'amount', 'currency',
            'paypal_payment_id', 'paypal_payer_id', 'paypal_payer_email',
            'status', 'payment_method', 'description'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return Payment.objects.create(user=user, **validated_data)
