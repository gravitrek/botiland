"""
Admin configuration for Gamification app.
"""

from django.contrib import admin
from .models import Badge, UserBadge, Quest, UserQuest, Leaderboard


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'rarity', 'xp_reward', 'times_awarded']
    list_filter = ['badge_type', 'rarity']
    search_fields = ['name', 'description']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at', 'is_featured']
    list_filter = ['is_featured', 'awarded_at']
    search_fields = ['user__email', 'badge__name']


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ['title', 'quest_type', 'xp_reward', 'credit_reward', 'start_date', 'end_date', 'is_active']
    list_filter = ['quest_type', 'is_active']
    search_fields = ['title', 'description']


@admin.register(UserQuest)
class UserQuestAdmin(admin.ModelAdmin):
    list_display = ['user', 'quest', 'progress', 'completed', 'completed_at']
    list_filter = ['completed']
    search_fields = ['user__email', 'quest__title']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'leaderboard_type', 'timeframe', 'is_active']
    list_filter = ['leaderboard_type', 'timeframe', 'is_active']
    search_fields = ['name']
