"""
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
