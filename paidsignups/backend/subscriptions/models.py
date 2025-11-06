from django.db import models
from django.conf import settings
import uuid


class Subscription(models.Model):
    """PayPal subscription tracking"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')

    # Plan info
    plan = models.CharField(
        max_length=20,
        choices=[
            ('FREE', 'Free'),
            ('BASIC', 'Basic'),
            ('PRO', 'Pro'),
            ('ENTERPRISE', 'Enterprise'),
        ]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # PayPal info
    paypal_subscription_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    paypal_order_id = models.CharField(max_length=255, null=True, blank=True)
    paypal_payer_id = models.CharField(max_length=255, null=True, blank=True)
    paypal_payer_email = models.EmailField(null=True, blank=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('ACTIVE', 'Active'),
            ('CANCELLED', 'Cancelled'),
            ('EXPIRED', 'Expired'),
            ('SUSPENDED', 'Suspended'),
        ],
        default='PENDING'
    )

    # Dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateTimeField(null=True, blank=True)

    # Cancellation
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan} ({self.status})"

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created_at']


class Payment(models.Model):
    """Individual payment records"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')

    # Payment info
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # PayPal info
    paypal_payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    paypal_payer_id = models.CharField(max_length=255, null=True, blank=True)
    paypal_payer_email = models.EmailField(null=True, blank=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('COMPLETED', 'Completed'),
            ('FAILED', 'Failed'),
            ('REFUNDED', 'Refunded'),
        ],
        default='PENDING'
    )

    # Metadata
    payment_method = models.CharField(max_length=50, default='PayPal')
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - ${self.amount} ({self.status})"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
