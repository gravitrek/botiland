"""
Models for Community - JoliTableau
Events, forums, discussions
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    """Art events - physical or virtual"""
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events',
        verbose_name=_('organisateur')
    )
    title = models.CharField(_('titre'), max_length=300)
    description = models.TextField(_('description'))
    event_type = models.CharField(
        _('type d\'événement'),
        max_length=50,
        choices=[
            ('PHYSICAL', _('Physique')),
            ('VIRTUAL', _('Virtuel')),
            ('HYBRID', _('Hybride')),
        ]
    )
    start_date = models.DateTimeField(_('date de début'))
    end_date = models.DateTimeField(_('date de fin'))
    location = models.CharField(_('lieu'), max_length=300, blank=True)
    virtual_link = models.URLField(_('lien virtuel'), blank=True)
    max_attendees = models.IntegerField(_('nombre max de participants'), null=True, blank=True)
    is_free = models.BooleanField(_('gratuit'), default=True)
    ticket_price = models.DecimalField(_('prix du billet'), max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)

    class Meta:
        verbose_name = _('événement')
        verbose_name_plural = _('événements')
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    """Event registration"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name=_('événement')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_registrations',
        verbose_name=_('utilisateur')
    )
    registered_at = models.DateTimeField(_('inscrit le'), auto_now_add=True)
    attended = models.BooleanField(_('a participé'), default=False)

    class Meta:
        verbose_name = _('inscription à un événement')
        verbose_name_plural = _('inscriptions à des événements')
        unique_together = ['event', 'user']
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.display_name} → {self.event.title}"
