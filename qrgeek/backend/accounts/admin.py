"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SubscriptionPlan, UserSubscription


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    list_display = [
        'email', 'username', 'full_name', 'company_name',
        'industry', 'is_verified', 'is_active', 'created_at'
    ]
    list_filter = ['is_verified', 'is_active', 'industry', 'created_at']
    search_fields = ['email', 'username', 'full_name', 'company_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'company_name', 'industry')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Verification', {'fields': ('is_verified', 'verification_token')}),
        ('Subscription', {'fields': ('subscription_plan',)}),
        ('Important Dates', {'fields': ('last_login', 'last_login_at', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['date_joined', 'last_login']


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin interface for SubscriptionPlan model."""
    list_display = [
        'name', 'price', 'billing_period', 'qr_limit',
        'scan_limit', 'is_active', 'is_featured', 'display_order'
    ]
    list_filter = ['billing_period', 'is_active', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'price']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'display_order')
        }),
        ('Pricing', {
            'fields': ('price', 'billing_period')
        }),
        ('Limits', {
            'fields': ('qr_limit', 'scan_limit')
        }),
        ('Features', {
            'fields': ('features',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for UserSubscription model."""
    list_display = [
        'user', 'plan', 'status', 'starts_at',
        'ends_at', 'auto_renew', 'created_at'
    ]
    list_filter = ['status', 'auto_renew', 'plan', 'created_at']
    search_fields = ['user__email', 'user__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Subscription Details', {
            'fields': ('user', 'plan', 'status')
        }),
        ('Period', {
            'fields': ('starts_at', 'ends_at', 'cancelled_at')
        }),
        ('Billing', {
            'fields': ('auto_renew', 'payment_method')
        }),
    )

    readonly_fields = ['created_at', 'updated_at']
