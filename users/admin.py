"""
Admin configuration for Users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Friend, FriendRequest


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'level', 'xp', 'credits', 'subscription_tier', 'is_coach', 'date_joined']
    list_filter = ['subscription_tier', 'is_coach', 'verified_coach', 'is_staff', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'avatar', 'location', 'website')}),
        ('Gamification', {'fields': ('xp', 'level', 'current_streak', 'longest_streak')}),
        ('Credits & Subscription', {'fields': ('credits', 'credits_expiry', 'subscription_tier', 'subscription_start_date', 'subscription_end_date')}),
        ('Coaching', {'fields': ('is_coach', 'verified_coach', 'coach_bio', 'coach_hourly_rate_credits', 'coach_rating')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend', 'created_at']
    search_fields = ['user__email', 'friend__email']


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['from_user__email', 'to_user__email']
