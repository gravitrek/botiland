from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'subscription_plan', 'subscription_active', 'is_verified', 'created_at']
    list_filter = ['subscription_plan', 'subscription_active', 'is_verified', 'is_staff']
    search_fields = ['email', 'username', 'company_name']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('company_name', 'phone_number', 'website')}),
        ('Subscription', {'fields': ('subscription_plan', 'subscription_active', 'subscription_start_date', 'subscription_end_date')}),
        ('PayPal', {'fields': ('paypal_subscription_id', 'paypal_payer_id')}),
        ('Usage', {'fields': ('forms_created', 'landing_pages_created', 'leads_this_month')}),
        ('Verification', {'fields': ('is_verified',)}),
    )
