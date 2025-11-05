"""
Admin configuration for Goals app.
"""

from django.contrib import admin
from .models import Goal, Milestone, Action, Step, GoalLike


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'privacy', 'is_template', 'progress_percentage', 'completed', 'created_at']
    list_filter = ['privacy', 'is_template', 'is_premium_template', 'completed', 'category']
    search_fields = ['title', 'description', 'user__email']
    readonly_fields = ['progress_percentage', 'created_at', 'updated_at']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal', 'target_date', 'completed', 'xp_reward']
    list_filter = ['completed']
    search_fields = ['title', 'goal__title']


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['title', 'milestone', 'frequency', 'current_streak', 'best_streak']
    list_filter = ['frequency']
    search_fields = ['title', 'milestone__title']


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['title', 'action', 'completed', 'order']
    list_filter = ['completed']
    search_fields = ['title']


@admin.register(GoalLike)
class GoalLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal', 'created_at']
    search_fields = ['user__email', 'goal__title']
