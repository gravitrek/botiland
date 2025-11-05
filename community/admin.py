"""
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
