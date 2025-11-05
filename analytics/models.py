"""
Analytics models for MegaGoals platform.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class GoalAnalytics(models.Model):
    """Goal analytics and stats model."""

    goal = models.OneToOneField('goals.Goal', on_delete=models.CASCADE, related_name='analytics')

    # Completion stats
    total_actions = models.PositiveIntegerField(_('total actions'), default=0)
    completed_actions = models.PositiveIntegerField(_('completed actions'), default=0)
    completion_rate = models.DecimalField(_('completion rate'), max_digits=5, decimal_places=2, default=0.00)

    # Time stats
    average_completion_time_days = models.PositiveIntegerField(_('average completion time (days)'), default=0)
    estimated_completion_date = models.DateField(_('estimated completion date'), null=True, blank=True)

    # Engagement
    total_views = models.PositiveIntegerField(_('total views'), default=0)
    unique_visitors = models.PositiveIntegerField(_('unique visitors'), default=0)

    # Activity patterns
    most_productive_day = models.CharField(_('most productive day'), max_length=20, blank=True)
    most_productive_time = models.CharField(_('most productive time'), max_length=20, blank=True)
    consistency_score = models.DecimalField(_('consistency score'), max_digits=5, decimal_places=2, default=0.00)

    last_calculated_at = models.DateTimeField(_('last calculated at'), auto_now=True)

    class Meta:
        verbose_name = _('goal analytics')
        verbose_name_plural = _('goal analytics')

    def __str__(self):
        return f'Analytics for {self.goal}'


class UserAnalytics(models.Model):
    """User analytics and stats model."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analytics')

    # Goal stats
    total_goals = models.PositiveIntegerField(_('total goals'), default=0)
    active_goals = models.PositiveIntegerField(_('active goals'), default=0)
    completed_goals = models.PositiveIntegerField(_('completed goals'), default=0)
    goal_completion_rate = models.DecimalField(_('goal completion rate'), max_digits=5, decimal_places=2, default=0.00)

    # Action stats
    total_actions_completed = models.PositiveIntegerField(_('total actions completed'), default=0)
    total_milestones_completed = models.PositiveIntegerField(_('total milestones completed'), default=0)

    # Time stats
    days_active = models.PositiveIntegerField(_('days active'), default=0)
    most_productive_day = models.CharField(_('most productive day'), max_length=20, blank=True)
    most_productive_hour = models.PositiveIntegerField(_('most productive hour'), default=0)

    # Engagement
    average_daily_actions = models.DecimalField(_('average daily actions'), max_digits=5, decimal_places=2, default=0.00)
    consistency_score = models.DecimalField(_('consistency score'), max_digits=5, decimal_places=2, default=0.00)

    # Social
    total_cheers_given = models.PositiveIntegerField(_('total cheers given'), default=0)
    total_cheers_received = models.PositiveIntegerField(_('total cheers received'), default=0)
    total_comments = models.PositiveIntegerField(_('total comments'), default=0)

    # Templates
    templates_created = models.PositiveIntegerField(_('templates created'), default=0)
    templates_downloaded = models.PositiveIntegerField(_('templates downloaded'), default=0)

    last_calculated_at = models.DateTimeField(_('last calculated at'), auto_now=True)

    class Meta:
        verbose_name = _('user analytics')
        verbose_name_plural = _('user analytics')

    def __str__(self):
        return f'Analytics for {self.user}'


class ActivityLog(models.Model):
    """Activity log for tracking user actions."""

    ACTIVITY_TYPES = (
        ('goal_created', _('Goal Created')),
        ('goal_completed', _('Goal Completed')),
        ('milestone_completed', _('Milestone Completed')),
        ('action_completed', _('Action Completed')),
        ('badge_earned', _('Badge Earned')),
        ('level_up', _('Level Up')),
        ('template_created', _('Template Created')),
        ('template_used', _('Template Used')),
        ('cheer_given', _('Cheer Given')),
        ('comment_posted', _('Comment Posted')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(_('activity type'), max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(_('description'))

    # Related objects (generic)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)

    # Metadata
    metadata = models.JSONField(_('metadata'), default=dict)

    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        verbose_name = _('activity log')
        verbose_name_plural = _('activity logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['activity_type', '-timestamp']),
        ]

    def __str__(self):
        return f'{self.user} - {self.get_activity_type_display()}'
