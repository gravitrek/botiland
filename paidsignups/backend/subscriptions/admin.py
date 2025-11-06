from django.contrib import admin
from .models import Subscription, Payment


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'amount', 'start_date', 'end_date']
    list_filter = ['plan', 'status', 'created_at']
    search_fields = ['user__email', 'paypal_subscription_id']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__email', 'paypal_payment_id']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
