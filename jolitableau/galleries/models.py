"""
Models for Galleries - JoliTableau
Gallery pages, exhibitions, virtual tours
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Gallery(models.Model):
    """Gallery page for artists/galleries"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='galleries',
        verbose_name=_('propriétaire')
    )
    name = models.CharField(_('nom'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    cover_image = models.ImageField(_('image de couverture'), upload_to='galleries/', blank=True)
    layout_type = models.CharField(
        _('type de mise en page'),
        max_length=20,
        choices=[
            ('GRID', _('Grille')),
            ('CAROUSEL', _('Carrousel')),
            ('MASONRY', _('Mosaïque')),
        ],
        default='GRID'
    )
    is_public = models.BooleanField(_('public'), default=True)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('galerie')
        verbose_name_plural = _('galeries')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.owner.id}")
        super().save(*args, **kwargs)


class Exhibition(models.Model):
    """Virtual exhibition"""
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.CASCADE,
        related_name='exhibitions',
        verbose_name=_('galerie')
    )
    title = models.CharField(_('titre'), max_length=300)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    start_date = models.DateField(_('date de début'))
    end_date = models.DateField(_('date de fin'))
    is_virtual = models.BooleanField(_('virtuel'), default=True)
    artworks = models.ManyToManyField(
        'artworks.Artwork',
        related_name='exhibitions',
        verbose_name=_('œuvres')
    )
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)

    class Meta:
        verbose_name = _('exposition')
        verbose_name_plural = _('expositions')
        ordering = ['-start_date']

    def __str__(self):
        return self.title
