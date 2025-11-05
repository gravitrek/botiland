"""
Models for Payments - JoliTableau
Payment transactions, subscriptions, monetization
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):
    """Payment transaction"""
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        COMPLETED = 'COMPLETED', _('Complété')
        FAILED = 'FAILED', _('Échec')
        REFUNDED = 'REFUNDED', _('Remboursé')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name=_('utilisateur')
    )
    amount = models.DecimalField(_('montant'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('devise'), max_length=3, default='EUR')
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment_method = models.CharField(_('méthode de paiement'), max_length=50)
    transaction_id = models.CharField(_('ID transaction'), max_length=200, unique=True)
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    completed_at = models.DateTimeField(_('complété le'), null=True, blank=True)

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.amount} {self.currency}"


class Subscription(models.Model):
    """Premium subscription (domain, boost, etc.)"""
    class SubscriptionType(models.TextChoices):
        DOMAIN = 'DOMAIN', _('Domaine personnalisé')
        BOOST = 'BOOST', _('Boost visibilité')
        WHATSAPP = 'WHATSAPP', _('WhatsApp forfait')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name=_('utilisateur')
    )
    subscription_type = models.CharField(
        _('type d\'abonnement'),
        max_length=20,
        choices=SubscriptionType.choices
    )
    is_active = models.BooleanField(_('actif'), default=True)
    monthly_price = models.DecimalField(_('prix mensuel'), max_digits=6, decimal_places=2)
    start_date = models.DateField(_('date de début'), auto_now_add=True)
    end_date = models.DateField(_('date de fin'), null=True, blank=True)
    auto_renew = models.BooleanField(_('renouvellement automatique'), default=True)

    class Meta:
        verbose_name = _('abonnement')
        verbose_name_plural = _('abonnements')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.email} - {self.subscription_type}"
