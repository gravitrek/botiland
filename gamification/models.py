"""
Gamification models for MegaGoals platform.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Badge(models.Model):
    """Badge model for achievements."""

    BADGE_TYPES = (
        ('streak', _('Streak')),
        ('milestone', _('Milestone')),
        ('community', _('Community')),
        ('template', _('Template')),
        ('coaching', _('Coaching')),
        ('special', _('Special')),
    )

    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'))
    badge_type = models.CharField(_('badge type'), max_length=20, choices=BADGE_TYPES, default='special')
    icon = models.CharField(_('icon'), max_length=50, default='🏆')
    icon_image = models.ImageField(_('icon image'), upload_to='badges/', blank=True, null=True)

    # Requirements
    requirement_type = models.CharField(_('requirement type'), max_length=50)
    requirement_value = models.PositiveIntegerField(_('requirement value'), default=0)

    # Stats
    rarity = models.CharField(_('rarity'), max_length=20, default='common')
    xp_reward = models.PositiveIntegerField(_('XP reward'), default=0)
    times_awarded = models.PositiveIntegerField(_('times awarded'), default=0)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('badge')
        verbose_name_plural = _('badges')
        ordering = ['name']

    def __str__(self):
        return f'{self.icon} {self.name}'


class UserBadge(models.Model):
    """User badge award model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    awarded_at = models.DateTimeField(_('awarded at'), auto_now_add=True)

    # Display settings
    is_featured = models.BooleanField(_('is featured'), default=False)
    display_order = models.PositiveIntegerField(_('display order'), default=0)

    class Meta:
        verbose_name = _('user badge')
        verbose_name_plural = _('user badges')
        unique_together = ('user', 'badge')
        ordering = ['-awarded_at']

    def __str__(self):
        return f'{self.user} - {self.badge}'


class Quest(models.Model):
    """Daily/Weekly quest model."""

    QUEST_TYPES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('special', _('Special')),
    )

    title = models.CharField(_('title'), max_length=150)
    description = models.TextField(_('description'))
    quest_type = models.CharField(_('quest type'), max_length=20, choices=QUEST_TYPES, default='daily')

    # Requirements
    requirement_action = models.CharField(_('requirement action'), max_length=100)
    requirement_count = models.PositiveIntegerField(_('requirement count'), default=1)

    # Rewards
    xp_reward = models.PositiveIntegerField(_('XP reward'), default=50)
    credit_reward = models.PositiveIntegerField(_('credit reward'), default=0)

    # Availability
    start_date = models.DateTimeField(_('start date'))
    end_date = models.DateTimeField(_('end date'))
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('quest')
        verbose_name_plural = _('quests')
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.get_quest_type_display()}: {self.title}'


class UserQuest(models.Model):
    """User quest progress model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quests')
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='user_quests')

    # Progress
    progress = models.PositiveIntegerField(_('progress'), default=0)
    completed = models.BooleanField(_('completed'), default=False)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('user quest')
        verbose_name_plural = _('user quests')
        unique_together = ('user', 'quest')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.quest}'


class Leaderboard(models.Model):
    """Leaderboard model."""

    LEADERBOARD_TYPES = (
        ('global', _('Global')),
        ('category', _('Category')),
        ('community', _('Community')),
    )

    TIMEFRAMES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('all_time', _('All Time')),
    )

    name = models.CharField(_('name'), max_length=100)
    leaderboard_type = models.CharField(_('leaderboard type'), max_length=20, choices=LEADERBOARD_TYPES, default='global')
    timeframe = models.CharField(_('timeframe'), max_length=20, choices=TIMEFRAMES, default='all_time')

    # Filter criteria
    category = models.CharField(_('category'), max_length=50, blank=True)
    community_id = models.PositiveIntegerField(_('community ID'), null=True, blank=True)

    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('leaderboard')
        verbose_name_plural = _('leaderboards')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_timeframe_display()})'
