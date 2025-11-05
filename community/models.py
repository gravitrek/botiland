"""
Community models for MegaGoals platform.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Community(models.Model):
    """Community/Group model."""

    PRIVACY_CHOICES = (
        ('public', _('Public')),
        ('private', _('Private')),
        ('paid', _('Paid')),
    )

    name = models.CharField(_('name'), max_length=150)
    description = models.TextField(_('description'))
    cover_image = models.ImageField(_('cover image'), upload_to='communities/', blank=True, null=True)
    category = models.CharField(_('category'), max_length=50)

    # Creator/Admin
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_communities')
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='admin_communities', blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CommunityMembership', related_name='communities')

    # Settings
    privacy = models.CharField(_('privacy'), max_length=20, choices=PRIVACY_CHOICES, default='public')
    is_auto_created = models.BooleanField(_('is auto created'), default=False)  # Auto-created by goal category

    # Paid community settings
    entry_cost_credits = models.PositiveIntegerField(_('entry cost (credits)'), default=0)
    monthly_cost_credits = models.PositiveIntegerField(_('monthly cost (credits)'), default=0)

    # Stats
    member_count = models.PositiveIntegerField(_('member count'), default=0)
    post_count = models.PositiveIntegerField(_('post count'), default=0)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('community')
        verbose_name_plural = _('communities')
        ordering = ['-member_count', '-created_at']

    def __str__(self):
        return self.name


class CommunityMembership(models.Model):
    """Community membership model."""

    ROLE_CHOICES = (
        ('member', _('Member')),
        ('moderator', _('Moderator')),
        ('admin', _('Admin')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default='member')

    joined_at = models.DateTimeField(_('joined at'), auto_now_add=True)
    last_payment_date = models.DateTimeField(_('last payment date'), null=True, blank=True)

    class Meta:
        verbose_name = _('community membership')
        verbose_name_plural = _('community memberships')
        unique_together = ('user', 'community')
        ordering = ['-joined_at']

    def __str__(self):
        return f'{self.user} in {self.community}'


class Post(models.Model):
    """Community post model."""

    POST_TYPES = (
        ('text', _('Text')),
        ('goal_share', _('Goal Share')),
        ('achievement', _('Achievement')),
        ('question', _('Question')),
    )

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    post_type = models.CharField(_('post type'), max_length=20, choices=POST_TYPES, default='text')
    content = models.TextField(_('content'))

    # Related objects
    related_goal = models.ForeignKey('goals.Goal', on_delete=models.SET_NULL, null=True, blank=True)

    # Engagement
    likes_count = models.PositiveIntegerField(_('likes count'), default=0)
    comments_count = models.PositiveIntegerField(_('comments count'), default=0)
    is_pinned = models.BooleanField(_('is pinned'), default=False)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f'{self.author} - {self.content[:50]}'


class Comment(models.Model):
    """Comment model for goals and posts."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')

    # Can comment on either a post or goal
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    goal = models.ForeignKey('goals.Goal', on_delete=models.CASCADE, null=True, blank=True, related_name='comments')

    content = models.TextField(_('content'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    likes_count = models.PositiveIntegerField(_('likes count'), default=0)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user} - {self.content[:50]}'


class Cheer(models.Model):
    """Cheer/Reaction model for actions."""

    EMOJI_CHOICES = (
        ('🎉', '🎉'),
        ('💪', '💪'),
        ('🔥', '🔥'),
        ('👏', '👏'),
        ('⭐', '⭐'),
        ('❤️', '❤️'),
        ('🚀', '🚀'),
        ('💯', '💯'),
    )

    action = models.ForeignKey('goals.Action', on_delete=models.CASCADE, related_name='cheers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cheers')
    emoji = models.CharField(_('emoji'), max_length=10, choices=EMOJI_CHOICES, default='🎉')

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('cheer')
        verbose_name_plural = _('cheers')
        unique_together = ('action', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} cheers {self.action} with {self.emoji}'


class Notification(models.Model):
    """Notification model."""

    NOTIFICATION_TYPES = (
        ('like', _('Like')),
        ('comment', _('Comment')),
        ('cheer', _('Cheer')),
        ('follow', _('Follow')),
        ('milestone', _('Milestone')),
        ('badge', _('Badge')),
        ('quest_complete', _('Quest Complete')),
        ('friend_request', _('Friend Request')),
        ('community_invite', _('Community Invite')),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')

    notification_type = models.CharField(_('notification type'), max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(_('title'), max_length=200)
    message = models.TextField(_('message'))

    # Related objects (generic)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)

    read = models.BooleanField(_('read'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.recipient} - {self.title}'
