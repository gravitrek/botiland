"""
Models for Communications - JoliTableau
Mailing lists, WhatsApp broadcast, notifications
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class MailingList(models.Model):
    """
    Mailing list for artists/galleries to communicate with followers
    RGPD compliant - emails anonymized, managed by JoliTableau
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailing_lists',
        verbose_name=_('propriétaire')
    )
    name = models.CharField(_('nom'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('actif'), default=True)

    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('liste de diffusion')
        verbose_name_plural = _('listes de diffusion')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.owner.display_name}"

    @property
    def subscriber_count(self):
        return self.subscribers.filter(is_subscribed=True).count()


class Subscriber(models.Model):
    """
    Subscriber to a mailing list
    Double opt-in, RGPD compliant
    """
    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name=_('liste de diffusion')
    )
    email = models.EmailField(_('email'))
    full_name = models.CharField(_('nom complet'), max_length=200, blank=True)

    # Subscriptions
    is_subscribed = models.BooleanField(_('abonné'), default=True)
    whatsapp_optin = models.BooleanField(_('opt-in WhatsApp'), default=False)
    whatsapp_number = models.CharField(_('numéro WhatsApp'), max_length=20, blank=True)

    # RGPD Compliance
    consent_given = models.BooleanField(_('consentement donné'), default=False)
    consent_date = models.DateTimeField(_('date du consentement'), null=True, blank=True)
    ip_address = models.GenericIPAddressField(_('adresse IP'), null=True, blank=True)

    # Timestamps
    subscribed_at = models.DateTimeField(_('abonné le'), auto_now_add=True)
    unsubscribed_at = models.DateTimeField(_('désabonné le'), null=True, blank=True)

    class Meta:
        verbose_name = _('abonné')
        verbose_name_plural = _('abonnés')
        unique_together = ['mailing_list', 'email']
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.email} → {self.mailing_list.name}"


class EmailCampaign(models.Model):
    """
    Email campaign sent to mailing list
    """
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Brouillon')
        SCHEDULED = 'SCHEDULED', _('Programmé')
        SENDING = 'SENDING', _('En cours d\'envoi')
        SENT = 'SENT', _('Envoyé')
        FAILED = 'FAILED', _('Échec')

    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        related_name='campaigns',
        verbose_name=_('liste de diffusion')
    )
    subject = models.CharField(_('sujet'), max_length=300)
    content = models.TextField(_('contenu'))
    html_content = models.TextField(_('contenu HTML'), blank=True)

    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # Scheduling
    scheduled_at = models.DateTimeField(_('programmé pour'), null=True, blank=True)
    sent_at = models.DateTimeField(_('envoyé le'), null=True, blank=True)

    # Statistics
    total_recipients = models.IntegerField(_('nombre de destinataires'), default=0)
    sent_count = models.IntegerField(_('envoyés'), default=0)
    opened_count = models.IntegerField(_('ouverts'), default=0)
    clicked_count = models.IntegerField(_('cliqués'), default=0)
    bounced_count = models.IntegerField(_('rejetés'), default=0)

    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('campagne email')
        verbose_name_plural = _('campagnes email')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.mailing_list.name}"


class WhatsAppBroadcast(models.Model):
    """
    WhatsApp broadcast message (via Twilio)
    Paid feature - configured price per message
    """
    class Status(models.TextChoices):
        PENDING_APPROVAL = 'PENDING_APPROVAL', _('En attente d\'approbation')
        APPROVED = 'APPROVED', _('Approuvé')
        REJECTED = 'REJECTED', _('Rejeté')
        SENDING = 'SENDING', _('En cours d\'envoi')
        SENT = 'SENT', _('Envoyé')
        FAILED = 'FAILED', _('Échec')

    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        related_name='whatsapp_broadcasts',
        verbose_name=_('liste de diffusion')
    )
    message = models.TextField(_('message'), max_length=1600)  # WhatsApp limit

    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING_APPROVAL
    )

    # Admin approval (to prevent spam)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_broadcasts',
        verbose_name=_('approuvé par')
    )
    approved_at = models.DateTimeField(_('approuvé le'), null=True, blank=True)
    rejection_reason = models.TextField(_('raison du rejet'), blank=True)

    # Scheduling
    scheduled_at = models.DateTimeField(_('programmé pour'), null=True, blank=True)
    sent_at = models.DateTimeField(_('envoyé le'), null=True, blank=True)

    # Statistics
    total_recipients = models.IntegerField(_('nombre de destinataires'), default=0)
    sent_count = models.IntegerField(_('envoyés'), default=0)
    delivered_count = models.IntegerField(_('délivrés'), default=0)
    failed_count = models.IntegerField(_('échecs'), default=0)

    # Pricing
    cost_per_message = models.DecimalField(_('coût par message'), max_digits=5, decimal_places=2, default=0.05)
    total_cost = models.DecimalField(_('coût total'), max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('broadcast WhatsApp')
        verbose_name_plural = _('broadcasts WhatsApp')
        ordering = ['-created_at']

    def __str__(self):
        return f"WhatsApp: {self.mailing_list.name} ({self.status})"

    def calculate_cost(self):
        """Calculate total cost of broadcast"""
        optin_count = self.mailing_list.subscribers.filter(
            is_subscribed=True,
            whatsapp_optin=True
        ).count()
        self.total_recipients = optin_count
        self.total_cost = optin_count * self.cost_per_message
        self.save(update_fields=['total_recipients', 'total_cost'])
