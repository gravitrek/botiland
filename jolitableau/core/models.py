"""
Models for the Core app - JoliTableau
Handles QR codes, custom domains, multi-tenant functionality
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import qrcode
from io import BytesIO
from django.core.files import File
import uuid


class CustomDomain(models.Model):
    """
    Custom domain configuration for artists/galleries (white-label)
    Supports both subdomain (free) and custom domains (paid)
    """

    class DomainType(models.TextChoices):
        SUBDOMAIN = 'SUBDOMAIN', _('Sous-domaine (gratuit)')
        CUSTOM = 'CUSTOM', _('Domaine personnalisé (payant)')

    class DomainStatus(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        ACTIVE = 'ACTIVE', _('Actif')
        SUSPENDED = 'SUSPENDED', _('Suspendu')
        EXPIRED = 'EXPIRED', _('Expiré')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='custom_domains',
        verbose_name=_('utilisateur')
    )

    # Domain Configuration
    domain = models.CharField(_('domaine'), max_length=255, unique=True)
    domain_type = models.CharField(
        _('type de domaine'),
        max_length=20,
        choices=DomainType.choices,
        default=DomainType.SUBDOMAIN
    )
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=DomainStatus.choices,
        default=DomainStatus.PENDING
    )

    # SSL Certificate
    ssl_enabled = models.BooleanField(_('SSL activé'), default=False)
    ssl_issued_at = models.DateTimeField(_('SSL émis le'), null=True, blank=True)

    # Trial and Subscription
    is_trial = models.BooleanField(_('en période d\'essai'), default=True)
    trial_ends = models.DateTimeField(_('fin de l\'essai'), null=True, blank=True)
    subscription_active = models.BooleanField(_('abonnement actif'), default=False)

    # White-Label Branding
    custom_logo = models.ImageField(_('logo personnalisé'), upload_to='domains/logos/', blank=True, null=True)
    primary_color = models.CharField(_('couleur primaire'), max_length=7, default='#000000')
    secondary_color = models.CharField(_('couleur secondaire'), max_length=7, default='#D4AF37')  # Gold
    show_jolitableau_branding = models.BooleanField(_('afficher la marque JoliTableau'), default=True)

    # SEO
    meta_title = models.CharField(_('titre meta'), max_length=200, blank=True)
    meta_description = models.TextField(_('description meta'), blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)
    activated_at = models.DateTimeField(_('activé le'), null=True, blank=True)

    class Meta:
        verbose_name = _('domaine personnalisé')
        verbose_name_plural = _('domaines personnalisés')
        ordering = ['-created_at']

    def __str__(self):
        return self.domain

    def save(self, *args, **kwargs):
        # Set trial end date if it's a new domain
        if not self.pk and self.is_trial and not self.trial_ends:
            self.trial_ends = timezone.now() + timedelta(days=settings.DOMAIN_TRIAL_PERIOD)
        super().save(*args, **kwargs)

    def activate(self):
        """Activate the domain"""
        self.status = self.DomainStatus.ACTIVE
        self.activated_at = timezone.now()
        self.save(update_fields=['status', 'activated_at'])

    def is_expired(self):
        """Check if trial has expired"""
        if self.is_trial and self.trial_ends:
            return timezone.now() > self.trial_ends
        return False

    @property
    def full_url(self):
        """Return full URL for this domain"""
        protocol = 'https' if self.ssl_enabled else 'http'
        return f"{protocol}://{self.domain}"


class QRCode(models.Model):
    """
    QR Code generator for artworks, galleries, exhibitions, profiles
    Automatically generated for each entity
    """

    class QRCodeType(models.TextChoices):
        ARTWORK = 'ARTWORK', _('Œuvre')
        GALLERY = 'GALLERY', _('Galerie')
        EXHIBITION = 'EXHIBITION', _('Exposition')
        PROFILE = 'PROFILE', _('Profil')
        EVENT = 'EVENT', _('Événement')

    # Universal identifier
    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, unique=True, editable=False)

    # QR Code Configuration
    qr_type = models.CharField(
        _('type de QR code'),
        max_length=20,
        choices=QRCodeType.choices
    )
    target_url = models.URLField(_('URL cible'), max_length=500)
    short_code = models.CharField(_('code court'), max_length=20, unique=True)

    # Owner
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='qr_codes',
        verbose_name=_('propriétaire')
    )

    # Generated Images (different formats)
    image_png = models.ImageField(_('image PNG'), upload_to='qrcodes/png/', blank=True, null=True)
    image_svg = models.FileField(_('image SVG'), upload_to='qrcodes/svg/', blank=True, null=True)

    # Customization
    foreground_color = models.CharField(_('couleur avant-plan'), max_length=7, default='#000000')
    background_color = models.CharField(_('couleur arrière-plan'), max_length=7, default='#FFFFFF')
    logo_image = models.ImageField(_('logo central'), upload_to='qrcodes/logos/', blank=True, null=True)

    # Analytics
    scan_count = models.IntegerField(_('nombre de scans'), default=0)
    last_scanned = models.DateTimeField(_('dernier scan'), null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)
    is_active = models.BooleanField(_('actif'), default=True)

    class Meta:
        verbose_name = _('QR code')
        verbose_name_plural = _('QR codes')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['uuid']),
        ]

    def __str__(self):
        return f"QR Code: {self.short_code} ({self.qr_type})"

    def generate_qr_image(self):
        """Generate QR code image"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.target_url)
        qr.make(fit=True)

        # Generate PNG
        img = qr.make_image(fill_color=self.foreground_color, back_color=self.background_color)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        filename = f"qr_{self.short_code}.png"
        self.image_png.save(filename, File(buffer), save=False)

    def record_scan(self):
        """Record a QR code scan"""
        self.scan_count += 1
        self.last_scanned = timezone.now()
        self.save(update_fields=['scan_count', 'last_scanned'])


class SiteSettings(models.Model):
    """
    Global site settings for JoliTableau
    Singleton model - only one instance should exist
    """

    # Site Information
    site_name = models.CharField(_('nom du site'), max_length=100, default='JoliTableau')
    tagline = models.CharField(_('slogan'), max_length=200, default='La galerie d\'art en ligne')
    description = models.TextField(_('description'), blank=True)

    # Contact
    contact_email = models.EmailField(_('email de contact'), default='contact@jolitableau.com')
    support_email = models.EmailField(_('email support'), default='support@jolitableau.com')
    phone = models.CharField(_('téléphone'), max_length=20, blank=True)

    # Social Media
    facebook_url = models.URLField(_('Facebook'), blank=True)
    instagram_url = models.URLField(_('Instagram'), blank=True)
    twitter_url = models.URLField(_('Twitter/X'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn'), blank=True)

    # Features Flags
    enable_marketplace = models.BooleanField(_('activer marketplace'), default=True)
    enable_auctions = models.BooleanField(_('activer enchères'), default=True)
    enable_custom_domains = models.BooleanField(_('activer domaines personnalisés'), default=True)
    enable_whatsapp_broadcast = models.BooleanField(_('activer WhatsApp broadcast'), default=True)
    maintenance_mode = models.BooleanField(_('mode maintenance'), default=False)

    # Pricing (configurable by admin)
    domain_monthly_price = models.DecimalField(
        _('prix domaine mensuel'),
        max_digits=6,
        decimal_places=2,
        default=9.99
    )
    boost_monthly_price = models.DecimalField(
        _('prix boost mensuel'),
        max_digits=6,
        decimal_places=2,
        default=4.99
    )
    whatsapp_message_price = models.DecimalField(
        _('prix message WhatsApp'),
        max_digits=5,
        decimal_places=2,
        default=0.05
    )
    fair_listing_price = models.DecimalField(
        _('prix listing foire'),
        max_digits=6,
        decimal_places=2,
        default=49.00
    )
    commission_rate = models.DecimalField(
        _('taux de commission'),
        max_digits=4,
        decimal_places=2,
        default=10.00,
        help_text=_('Pourcentage de commission sur les ventes')
    )

    # Conseil des Sages
    conseil_max_members = models.IntegerField(_('max membres conseil'), default=20)
    conseil_voting_enabled = models.BooleanField(_('votes conseil activés'), default=True)

    # Timestamps
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('paramètres du site')
        verbose_name_plural = _('paramètres du site')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Load site settings (create if doesn't exist)"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Newsletter(models.Model):
    """
    Newsletter subscriptions for the global JoliTableau newsletter
    Separate from artist/gallery mailing lists
    """

    email = models.EmailField(_('email'), unique=True)
    full_name = models.CharField(_('nom complet'), max_length=200, blank=True)
    preferred_language = models.CharField(
        _('langue préférée'),
        max_length=5,
        choices=[('fr', 'Français'), ('en', 'English'), ('es', 'Español')],
        default='fr'
    )

    # Preferences
    interested_in_artists = models.BooleanField(_('intéressé par les artistes'), default=True)
    interested_in_galleries = models.BooleanField(_('intéressé par les galeries'), default=True)
    interested_in_events = models.BooleanField(_('intéressé par les événements'), default=True)

    # Status
    is_active = models.BooleanField(_('actif'), default=True)
    subscribed_at = models.DateTimeField(_('abonné le'), auto_now_add=True)
    unsubscribed_at = models.DateTimeField(_('désabonné le'), null=True, blank=True)

    # RGPD
    consent_given = models.BooleanField(_('consentement donné'), default=True)
    consent_date = models.DateTimeField(_('date du consentement'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_('adresse IP'), null=True, blank=True)

    class Meta:
        verbose_name = _('abonné newsletter')
        verbose_name_plural = _('abonnés newsletter')
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

    def unsubscribe(self):
        """Unsubscribe from newsletter"""
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save(update_fields=['is_active', 'unsubscribed_at'])
