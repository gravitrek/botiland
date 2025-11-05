from django.contrib import admin
from .models import (
    Badge, UserBadge, Achievement, UserAchievement,
    PointsTransaction, Leaderboard, Reward, RewardRedemption
)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'points_reward', 'is_rare', 'is_active']
    list_filter = ['category', 'is_rare', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at', 'is_displayed']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'trigger_type', 'points', 'is_active']
    list_filter = ['trigger_type', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'unlocked_at']
    list_filter = ['achievement', 'unlocked_at']
    search_fields = ['user__username', 'achievement__name']


@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'points', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__username']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'period_type', 'rank', 'total_points']
    list_filter = ['period_type']
    search_fields = ['user__username']


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['name', 'points_cost', 'quantity_available', 'quantity_redeemed', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RewardRedemption)
class RewardRedemptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'reward', 'points_spent', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'reward__name']
