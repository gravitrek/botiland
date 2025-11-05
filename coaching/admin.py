"""
Admin configuration for Coaching app.
"""

from django.contrib import admin
from .models import CoachingSession, CoachAvailability


@admin.register(CoachingSession)
class CoachingSessionAdmin(admin.ModelAdmin):
    list_display = ['coach', 'client', 'scheduled_at', 'status', 'cost_credits', 'paid', 'client_rating']
    list_filter = ['status', 'paid']
    search_fields = ['coach__email', 'client__email', 'title']


@admin.register(CoachAvailability)
class CoachAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['coach', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active']
    search_fields = ['coach__email']
