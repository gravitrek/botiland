"""
Admin configuration for payments app.
"""
from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'amount', 'currency', 'status',
        'payment_method', 'created_at', 'completed_at'
    ]
    list_filter = ['status', 'payment_method', 'currency', 'created_at']
    search_fields = ['user__email', 'paypal_order_id', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'subscription', 'amount', 'currency', 'payment_method')
        }),
        ('PayPal Details', {
            'fields': ('paypal_order_id', 'paypal_payer_id', 'paypal_payment_id')
        }),
        ('Status', {
            'fields': ('status', 'description', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )
