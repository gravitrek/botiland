"""
Script to create admin registrations for all apps.
"""

ADMIN_TEMPLATES = {
    'users/admin.py': '''"""
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
''',

    'goals/admin.py': '''"""
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
''',

    'gamification/admin.py': '''"""
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
''',

    'community/admin.py': '''"""
Admin configuration for Community app.
"""

from django.contrib import admin
from .models import Community, CommunityMembership, Post, Comment, Cheer, Notification


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'privacy', 'member_count', 'post_count', 'created_at']
    list_filter = ['privacy', 'is_auto_created']
    search_fields = ['name', 'description', 'category']


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'role', 'joined_at']
    list_filter = ['role']
    search_fields = ['user__email', 'community__name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'community', 'post_type', 'likes_count', 'comments_count', 'is_pinned', 'created_at']
    list_filter = ['post_type', 'is_pinned']
    search_fields = ['content', 'author__email']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'likes_count', 'created_at']
    search_fields = ['content', 'user__email']


@admin.register(Cheer)
class CheerAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'emoji', 'created_at']
    list_filter = ['emoji']
    search_fields = ['user__email']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'notification_type', 'title', 'read', 'created_at']
    list_filter = ['notification_type', 'read']
    search_fields = ['recipient__email', 'sender__email', 'title']
''',

    'coaching/admin.py': '''"""
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
''',

    'payments/admin.py': '''"""
Admin configuration for Payments app.
"""

from django.contrib import admin
from .models import CreditTransaction, Payment, CreditPack, Subscription


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'credits', 'balance_after', 'transaction_type', 'reason', 'timestamp']
    list_filter = ['transaction_type']
    search_fields = ['user__email', 'reason']
    readonly_fields = ['timestamp']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_type', 'amount', 'credits_amount', 'status', 'created_at']
    list_filter = ['payment_type', 'status']
    search_fields = ['user__email', 'stripe_payment_intent_id']


@admin.register(CreditPack)
class CreditPackAdmin(admin.ModelAdmin):
    list_display = ['name', 'credits', 'bonus_credits', 'price', 'is_featured', 'is_active', 'display_order']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier', 'status', 'current_period_start', 'current_period_end']
    list_filter = ['tier', 'status']
    search_fields = ['user__email', 'stripe_subscription_id']
''',

    'ai_coach/admin.py': '''"""
Admin configuration for AI Coach app.
"""

from django.contrib import admin
from .models import AICoachConversation, AICoachMessage, AIInsight, AIReport


@admin.register(AICoachConversation)
class AICoachConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'related_goal', 'created_at']
    search_fields = ['user__email', 'title']


@admin.register(AICoachMessage)
class AICoachMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'content', 'created_at']
    list_filter = ['role']
    search_fields = ['content']


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ['user', 'insight_type', 'title', 'is_read', 'is_helpful', 'created_at']
    list_filter = ['insight_type', 'is_read', 'is_helpful']
    search_fields = ['user__email', 'title', 'content']


@admin.register(AIReport)
class AIReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'report_type', 'title', 'start_date', 'end_date', 'is_read']
    list_filter = ['report_type', 'is_read']
    search_fields = ['user__email', 'title']
''',

    'analytics/admin.py': '''"""
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
''',
}

# Write all admin files
for file_path, content in ADMIN_TEMPLATES.items():
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Created {file_path}")

print("All admin files created successfully!")
