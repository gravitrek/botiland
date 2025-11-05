"""
Admin configuration for Analytics app.
"""

from django.contrib import admin
from .models import GoalAnalytics, UserAnalytics, ActivityLog


@admin.register(GoalAnalytics)
class GoalAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['goal', 'completion_rate', 'total_actions', 'completed_actions', 'consistency_score']
    search_fields = ['goal__title']
    readonly_fields = ['last_calculated_at']


@admin.register(UserAnalytics)
class UserAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_goals', 'active_goals', 'completed_goals', 'goal_completion_rate', 'consistency_score']
    search_fields = ['user__email']
    readonly_fields = ['last_calculated_at']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description', 'timestamp']
    list_filter = ['activity_type']
    search_fields = ['user__email', 'description']
    readonly_fields = ['timestamp']
