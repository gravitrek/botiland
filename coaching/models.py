"""
Coaching models for MegaGoals platform.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CoachingSession(models.Model):
    """Coaching session booking model."""

    SESSION_STATUS = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )

    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coaching_sessions_as_coach')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coaching_sessions_as_client')

    # Session details
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    scheduled_at = models.DateTimeField(_('scheduled at'))
    duration_minutes = models.PositiveIntegerField(_('duration (minutes)'), default=60)

    # Status
    status = models.CharField(_('status'), max_length=20, choices=SESSION_STATUS, default='pending')

    # Payment
    cost_credits = models.PositiveIntegerField(_('cost (credits)'))
    paid = models.BooleanField(_('paid'), default=False)
    paid_at = models.DateTimeField(_('paid at'), null=True, blank=True)

    # Feedback
    client_rating = models.PositiveIntegerField(_('client rating'), null=True, blank=True)
    client_feedback = models.TextField(_('client feedback'), blank=True)
    coach_notes = models.TextField(_('coach notes'), blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('coaching session')
        verbose_name_plural = _('coaching sessions')
        ordering = ['-scheduled_at']

    def __str__(self):
        return f'{self.client} with {self.coach} - {self.scheduled_at}'

    def mark_completed(self):
        """Mark session as completed."""
        self.status = 'completed'
        self.save()

        # Update coach stats
        self.coach.coach_total_sessions += 1
        self.coach.save(update_fields=['coach_total_sessions'])


class CoachAvailability(models.Model):
    """Coach availability schedule model."""

    DAYS_OF_WEEK = (
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    )

    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availability_slots')
    day_of_week = models.IntegerField(_('day of week'), choices=DAYS_OF_WEEK)
    start_time = models.TimeField(_('start time'))
    end_time = models.TimeField(_('end time'))
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('coach availability')
        verbose_name_plural = _('coach availability')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f'{self.coach} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}'
