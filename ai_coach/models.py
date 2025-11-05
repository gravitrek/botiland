"""
AI Coach models for MegaGoals platform.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AICoachConversation(models.Model):
    """AI Coach conversation model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_conversations')
    title = models.CharField(_('title'), max_length=200, default='New Conversation')

    # Related goal (optional)
    related_goal = models.ForeignKey('goals.Goal', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('AI coach conversation')
        verbose_name_plural = _('AI coach conversations')
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user} - {self.title}'


class AICoachMessage(models.Model):
    """AI Coach message model."""

    ROLE_CHOICES = (
        ('user', _('User')),
        ('assistant', _('Assistant')),
        ('system', _('System')),
    )

    conversation = models.ForeignKey(AICoachConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES)
    content = models.TextField(_('content'))

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('AI coach message')
        verbose_name_plural = _('AI coach messages')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.role}: {self.content[:50]}'


class AIInsight(models.Model):
    """AI-generated insight model."""

    INSIGHT_TYPES = (
        ('progress', _('Progress')),
        ('suggestion', _('Suggestion')),
        ('pattern', _('Pattern')),
        ('milestone', _('Milestone')),
        ('warning', _('Warning')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_insights')
    insight_type = models.CharField(_('insight type'), max_length=20, choices=INSIGHT_TYPES, default='suggestion')

    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))

    # Related objects
    related_goal = models.ForeignKey('goals.Goal', on_delete=models.SET_NULL, null=True, blank=True)
    related_action = models.ForeignKey('goals.Action', on_delete=models.SET_NULL, null=True, blank=True)

    # User interaction
    is_read = models.BooleanField(_('is read'), default=False)
    is_helpful = models.BooleanField(_('is helpful'), null=True, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('AI insight')
        verbose_name_plural = _('AI insights')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.title}'


class AIReport(models.Model):
    """AI-generated weekly/monthly report model."""

    REPORT_TYPES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_reports')
    report_type = models.CharField(_('report type'), max_length=20, choices=REPORT_TYPES, default='weekly')

    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    summary = models.TextField(_('summary'), blank=True)

    # Stats
    total_actions_completed = models.PositiveIntegerField(_('total actions completed'), default=0)
    xp_earned = models.PositiveIntegerField(_('XP earned'), default=0)
    streak_maintained = models.PositiveIntegerField(_('streak maintained'), default=0)

    # Date range
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))

    is_read = models.BooleanField(_('is read'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('AI report')
        verbose_name_plural = _('AI reports')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.get_report_type_display()} ({self.start_date} to {self.end_date})'
