"""
Models for Verification - JoliTableau
Badges, certifications, verification requests
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class VerificationRequest(models.Model):
    """Request for account verification"""
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        APPROVED = 'APPROVED', _('Approuvé')
        REJECTED = 'REJECTED', _('Rejeté')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='verification_requests',
        verbose_name=_('utilisateur')
    )
    verification_type = models.CharField(
        _('type de vérification'),
        max_length=50,
        choices=[
            ('ARTIST', _('Artiste')),
            ('GALLERY', _('Galerie')),
            ('COLLECTOR', _('Collectionneur')),
        ]
    )
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    documents = models.FileField(_('documents'), upload_to='verification/', blank=True)
    notes = models.TextField(_('notes'), blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_verifications',
        verbose_name=_('examiné par')
    )
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    reviewed_at = models.DateTimeField(_('examiné le'), null=True, blank=True)

    class Meta:
        verbose_name = _('demande de vérification')
        verbose_name_plural = _('demandes de vérification')
        ordering = ['-created_at']

    def __str__(self):
        return f"Verification: {self.user.email} ({self.status})"
