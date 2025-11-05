"""
Models for Analytics - JoliTableau
Page views, statistics, tracking
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class PageView(models.Model):
    """Track page views for analytics"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='page_views',
        verbose_name=_('utilisateur')
    )
    page_url = models.CharField(_('URL de la page'), max_length=500)
    page_type = models.CharField(
        _('type de page'),
        max_length=50,
        choices=[
            ('ARTWORK', _('Œuvre')),
            ('GALLERY', _('Galerie')),
            ('PROFILE', _('Profil')),
            ('HOMEPAGE', _('Page d\'accueil')),
        ]
    )
    ip_address = models.GenericIPAddressField(_('adresse IP'), null=True, blank=True)
    user_agent = models.TextField(_('user agent'), blank=True)
    referrer = models.CharField(_('référent'), max_length=500, blank=True)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)

    class Meta:
        verbose_name = _('vue de page')
        verbose_name_plural = _('vues de page')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['page_type', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.page_url} - {self.created_at}"
