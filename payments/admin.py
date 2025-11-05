"""
Admin configuration for Payments app.
"""

from django.contrib import admin
from .models import CreditTransaction, Payment, CreditPack, Subscription


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'credits', 'balance_after', 'transaction_type', 'reason', 'timestamp']
    list_filter = ['transaction_type']
    search_fields = ['user__email', 'reason']
    readonly_fields = ['timestamp']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_type', 'amount', 'credits_amount', 'status', 'created_at']
    list_filter = ['payment_type', 'status']
    search_fields = ['user__email', 'stripe_payment_intent_id']


@admin.register(CreditPack)
class CreditPackAdmin(admin.ModelAdmin):
    list_display = ['name', 'credits', 'bonus_credits', 'price', 'is_featured', 'is_active', 'display_order']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier', 'status', 'current_period_start', 'current_period_end']
    list_filter = ['tier', 'status']
    search_fields = ['user__email', 'stripe_subscription_id']
