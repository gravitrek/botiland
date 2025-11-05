"""
Goals models for MegaGoals platform.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Goal(models.Model):
    """Main goal model - top level of the hierarchy."""

    PRIVACY_CHOICES = (
        ('private', _('Private')),
        ('friends', _('Friends Only')),
        ('public', _('Public')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    category = models.CharField(_('category'), max_length=50, blank=True)

    # Privacy and template settings
    privacy = models.CharField(_('privacy'), max_length=20, choices=PRIVACY_CHOICES, default='private')
    is_template = models.BooleanField(_('is template'), default=False)
    is_premium_template = models.BooleanField(_('is premium template'), default=False)
    template_credit_cost = models.PositiveIntegerField(_('template credit cost'), default=0)
    template_downloads = models.PositiveIntegerField(_('template downloads'), default=0)

    # Replication tracking
    original_goal = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replicas')

    # Progress tracking
    progress_percentage = models.DecimalField(_('progress percentage'), max_digits=5, decimal_places=2, default=0.00)
    completed = models.BooleanField(_('completed'), default=False)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

    # Stats
    likes_count = models.PositiveIntegerField(_('likes count'), default=0)
    cheers_count = models.PositiveIntegerField(_('cheers count'), default=0)
    comments_count = models.PositiveIntegerField(_('comments count'), default=0)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('goal')
        verbose_name_plural = _('goals')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'completed']),
            models.Index(fields=['is_template', 'privacy']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def update_progress(self):
        """Calculate and update goal progress based on milestones."""
        milestones = self.milestones.all()
        if not milestones:
            self.progress_percentage = 0
        else:
            completed_milestones = milestones.filter(completed=True).count()
            self.progress_percentage = (completed_milestones / milestones.count()) * 100

        # Check if goal is complete
        if self.progress_percentage == 100 and not self.completed:
            self.completed = True
            self.completed_at = timezone.now()

            # Award XP
            self.user.add_xp(settings.XP_REWARDS['GOAL_COMPLETE'])

        self.save(update_fields=['progress_percentage', 'completed', 'completed_at'])


class Milestone(models.Model):
    """Milestone model - second level of hierarchy."""

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(_('title'), max_length=150)
    description = models.TextField(_('description'), blank=True)
    target_date = models.DateField(_('target date'), null=True, blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    # Progress
    completed = models.BooleanField(_('completed'), default=False)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)
    xp_reward = models.PositiveIntegerField(_('XP reward'), default=50)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('milestone')
        verbose_name_plural = _('milestones')
        ordering = ['order', 'target_date']

    def __str__(self):
        return f'{self.goal.title} - {self.title}'

    def mark_complete(self):
        """Mark milestone as complete and award XP."""
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save()

            # Award XP
            self.goal.user.add_xp(self.xp_reward)

            # Update goal progress
            self.goal.update_progress()


class Action(models.Model):
    """Action model - third level of hierarchy (repeatable tasks)."""

    FREQUENCY_CHOICES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('custom', _('Custom')),
    )

    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='actions')
    title = models.CharField(_('title'), max_length=150)
    description = models.TextField(_('description'), blank=True)

    # Frequency settings
    frequency = models.CharField(_('frequency'), max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    custom_frequency_days = models.PositiveIntegerField(_('custom frequency (days)'), default=1)

    # Completion tracking
    completed_dates = models.JSONField(_('completed dates'), default=list)
    xp_per_completion = models.PositiveIntegerField(_('XP per completion'), default=10)
    current_streak = models.PositiveIntegerField(_('current streak'), default=0)
    best_streak = models.PositiveIntegerField(_('best streak'), default=0)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('action')
        verbose_name_plural = _('actions')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def mark_complete_today(self):
        """Mark action as complete for today."""
        today = timezone.now().date().isoformat()

        if today not in self.completed_dates:
            self.completed_dates.append(today)
            self.save()

            # Award XP
            self.milestone.goal.user.add_xp(self.xp_per_completion)

            # Update streak
            self.update_streak()

            # Update user's global streak
            self.milestone.goal.user.update_streak()

    def update_streak(self):
        """Update action streak based on completion dates."""
        if not self.completed_dates:
            self.current_streak = 0
            return

        sorted_dates = sorted(self.completed_dates, reverse=True)
        today = timezone.now().date().isoformat()

        streak = 0
        expected_date = timezone.now().date()

        for date_str in sorted_dates:
            if date_str == expected_date.isoformat():
                streak += 1
                expected_date -= timezone.timedelta(days=1)
            else:
                break

        self.current_streak = streak
        self.best_streak = max(self.best_streak, streak)
        self.save(update_fields=['current_streak', 'best_streak'])


class Step(models.Model):
    """Step model - optional fourth level (one-off tasks)."""

    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(_('title'), max_length=150)
    description = models.TextField(_('description'), blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    # Completion
    completed = models.BooleanField(_('completed'), default=False)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('step')
        verbose_name_plural = _('steps')
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

    def mark_complete(self):
        """Mark step as complete."""
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save()


class GoalLike(models.Model):
    """Goal like model."""

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goal_likes')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('goal like')
        verbose_name_plural = _('goal likes')
        unique_together = ('goal', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} likes {self.goal}'
