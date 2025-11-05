"""
Models for Marketplace - JoliTableau
Sales, auctions, orders
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """Purchase order for artwork"""
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        PAID = 'PAID', _('Payé')
        SHIPPED = 'SHIPPED', _('Expédié')
        DELIVERED = 'DELIVERED', _('Livré')
        CANCELLED = 'CANCELLED', _('Annulé')

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name=_('acheteur')
    )
    artwork = models.ForeignKey(
        'artworks.Artwork',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('œuvre')
    )
    price = models.DecimalField(_('prix'), max_digits=10, decimal_places=2)
    commission = models.DecimalField(_('commission'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('montant total'), max_digits=10, decimal_places=2)
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    paid_at = models.DateTimeField(_('payé le'), null=True, blank=True)

    class Meta:
        verbose_name = _('commande')
        verbose_name_plural = _('commandes')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} - {self.artwork.title}"


class Auction(models.Model):
    """Auction for artwork"""
    artwork = models.OneToOneField(
        'artworks.Artwork',
        on_delete=models.CASCADE,
        related_name='auction',
        verbose_name=_('œuvre')
    )
    starting_bid = models.DecimalField(_('enchère de départ'), max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(_('enchère actuelle'), max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(_('début'))
    end_date = models.DateTimeField(_('fin'))
    is_active = models.BooleanField(_('actif'), default=True)
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_auctions',
        verbose_name=_('gagnant')
    )

    class Meta:
        verbose_name = _('enchère')
        verbose_name_plural = _('enchères')
        ordering = ['-end_date']

    def __str__(self):
        return f"Auction: {self.artwork.title}"
