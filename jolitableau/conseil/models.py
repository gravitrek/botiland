"""
Models for Conseil des Sages - JoliTableau
Elite council voting system
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ConseilMember(models.Model):
    """Member of Conseil des Sages (max 20 members)"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conseil_membership',
        verbose_name=_('utilisateur')
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='conseil_invitations',
        verbose_name=_('invité par')
    )
    joined_at = models.DateTimeField(_('membre depuis'), auto_now_add=True)
    is_active = models.BooleanField(_('actif'), default=True)
    bio = models.TextField(_('biographie'), blank=True)

    class Meta:
        verbose_name = _('membre du conseil')
        verbose_name_plural = _('membres du conseil')
        ordering = ['joined_at']

    def __str__(self):
        return f"Sage: {self.user.display_name}"


class ArtworkVote(models.Model):
    """Weekly voting for artwork of the day/week"""
    artwork = models.ForeignKey(
        'artworks.Artwork',
        on_delete=models.CASCADE,
        related_name='conseil_votes',
        verbose_name=_('œuvre')
    )
    member = models.ForeignKey(
        ConseilMember,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_('membre')
    )
    vote_date = models.DateField(_('date du vote'), auto_now_add=True)
    comment = models.TextField(_('commentaire'), blank=True)

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        unique_together = ['artwork', 'member', 'vote_date']
        ordering = ['-vote_date']

    def __str__(self):
        return f"{self.member.user.display_name} → {self.artwork.title}"
