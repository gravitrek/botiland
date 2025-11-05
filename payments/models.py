"""
Payments models for MegaGoals platform.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class CreditTransaction(models.Model):
    """Credit transaction history model."""

    TRANSACTION_TYPES = (
        ('purchase', _('Purchase')),
        ('subscription', _('Subscription')),
        ('reward', _('Reward')),
        ('refund', _('Refund')),
        ('spend', _('Spend')),
        ('expired', _('Expired')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_transactions')
    credits = models.IntegerField(_('credits'))
    balance_after = models.IntegerField(_('balance after'), default=0)

    transaction_type = models.CharField(_('transaction type'), max_length=20, choices=TRANSACTION_TYPES, default='spend')
    reason = models.CharField(_('reason'), max_length=200)
    description = models.TextField(_('description'), blank=True)

    # Related payment
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)

    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        verbose_name = _('credit transaction')
        verbose_name_plural = _('credit transactions')
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user} - {self.credits} credits ({self.reason})'


class Payment(models.Model):
    """Payment model for credit purchases and subscriptions."""

    PAYMENT_STATUS = (
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    )

    PAYMENT_TYPE = (
        ('credits', _('Credits')),
        ('subscription', _('Subscription')),
        ('coaching', _('Coaching')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')

    # Payment details
    payment_type = models.CharField(_('payment type'), max_length=20, choices=PAYMENT_TYPE, default='credits')
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='USD')

    # Credits (if applicable)
    credits_amount = models.PositiveIntegerField(_('credits amount'), default=0)

    # Stripe
    stripe_payment_intent_id = models.CharField(_('Stripe payment intent ID'), max_length=255, blank=True)
    stripe_charge_id = models.CharField(_('Stripe charge ID'), max_length=255, blank=True)

    # Status
    status = models.CharField(_('status'), max_length=20, choices=PAYMENT_STATUS, default='pending')

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - ${self.amount} ({self.status})'


class CreditPack(models.Model):
    """Credit pack/package model for sale."""

    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    credits = models.PositiveIntegerField(_('credits'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='USD')

    # Bonus
    bonus_credits = models.PositiveIntegerField(_('bonus credits'), default=0)

    # Display
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    display_order = models.PositiveIntegerField(_('display order'), default=0)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('credit pack')
        verbose_name_plural = _('credit packs')
        ordering = ['display_order', 'price']

    def __str__(self):
        return f'{self.name} - {self.credits} credits (${self.price})'

    def get_total_credits(self):
        """Get total credits including bonus."""
        return self.credits + self.bonus_credits


class Subscription(models.Model):
    """Subscription model."""

    SUBSCRIPTION_STATUS = (
        ('active', _('Active')),
        ('cancelled', _('Cancelled')),
        ('expired', _('Expired')),
        ('past_due', _('Past Due')),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription_model')
    tier = models.CharField(_('tier'), max_length=20)

    # Stripe
    stripe_subscription_id = models.CharField(_('Stripe subscription ID'), max_length=255, unique=True)
    stripe_customer_id = models.CharField(_('Stripe customer ID'), max_length=255)

    # Status
    status = models.CharField(_('status'), max_length=20, choices=SUBSCRIPTION_STATUS, default='active')

    # Dates
    start_date = models.DateTimeField(_('start date'), auto_now_add=True)
    current_period_start = models.DateTimeField(_('current period start'))
    current_period_end = models.DateTimeField(_('current period end'))
    cancelled_at = models.DateTimeField(_('cancelled at'), null=True, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.tier} ({self.status})'
