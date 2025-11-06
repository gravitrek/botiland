"""
QR Code models for QRGeek platform.
"""
import uuid
import shortuuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Tag(models.Model):
    """Tags for organizing QR codes."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'slug']

    def __str__(self):
        return self.name


class QRCode(models.Model):
    """Main QR Code model."""

    QR_TYPE_CHOICES = [
        ('url', 'URL / Website'),
        ('vcard', 'vCard / Contact'),
        ('text', 'Plain Text'),
        ('email', 'Email Address'),
        ('sms', 'SMS Message'),
        ('phone', 'Phone Number'),
        ('wifi', 'WiFi Credentials'),
        ('location', 'GPS Location'),
        ('event', 'Calendar Event'),
        ('app', 'App Store Link'),
        ('pdf', 'PDF Document'),
        ('menu', 'Restaurant Menu'),
        ('product', 'Product Info'),
        ('social', 'Social Media'),
    ]

    FORMAT_CHOICES = [
        ('png', 'PNG'),
        ('svg', 'SVG'),
        ('pdf', 'PDF'),
        ('eps', 'EPS'),
    ]

    ERROR_CORRECTION_CHOICES = [
        ('L', 'Low (7%)'),
        ('M', 'Medium (15%)'),
        ('Q', 'Quartile (25%)'),
        ('H', 'High (30%)'),
    ]

    # Basic Info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='qr_codes'
    )
    name = models.CharField(_('name'), max_length=255)
    qr_type = models.CharField(
        _('QR type'),
        max_length=20,
        choices=QR_TYPE_CHOICES,
        default='url'
    )

    # Content (flexible JSON structure based on qr_type)
    content = models.JSONField(_('content'))

    # URL Shortening
    short_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        help_text='Shortened URL code for tracking'
    )
    custom_domain = models.CharField(
        max_length=255,
        blank=True,
        help_text='Custom domain for short URL'
    )

    # Customization
    foreground_color = models.CharField(
        _('foreground color'),
        max_length=7,
        default='#000000',
        help_text='Hex color code'
    )
    background_color = models.CharField(
        _('background color'),
        max_length=7,
        default='#FFFFFF',
        help_text='Hex color code'
    )
    logo = models.ImageField(
        _('logo'),
        upload_to='qr_logos/',
        blank=True,
        null=True,
        help_text='Logo to embed in QR code center'
    )
    size = models.IntegerField(
        _('size'),
        default=400,
        validators=[
            MinValueValidator(200),
            MaxValueValidator(2000)
        ],
        help_text='Size in pixels'
    )
    format = models.CharField(
        _('format'),
        max_length=10,
        choices=FORMAT_CHOICES,
        default='png'
    )
    error_correction = models.CharField(
        _('error correction'),
        max_length=1,
        choices=ERROR_CORRECTION_CHOICES,
        default='M'
    )

    # Generated QR Code Files
    qr_image = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        null=True
    )

    # Tracking & Analytics
    enable_tracking = models.BooleanField(_('enable tracking'), default=True)
    is_active = models.BooleanField(_('is active'), default=True)
    expires_at = models.DateTimeField(_('expires at'), null=True, blank=True)

    # Statistics
    total_scans = models.IntegerField(_('total scans'), default=0)
    unique_scans = models.IntegerField(_('unique scans'), default=0)
    last_scanned_at = models.DateTimeField(_('last scanned'), null=True, blank=True)

    # Organization
    tags = models.ManyToManyField(Tag, blank=True, related_name='qr_codes')
    folder = models.CharField(max_length=255, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'QR Code'
        verbose_name_plural = 'QR Codes'
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_qr_type_display()})"

    def save(self, *args, **kwargs):
        # Generate short code if not exists
        if not self.short_code:
            self.short_code = shortuuid.ShortUUID().random(length=7)

        super().save(*args, **kwargs)

    @property
    def short_url(self):
        """Get the short URL for this QR code."""
        domain = self.custom_domain or settings.SHORT_URL_DOMAIN
        return f"https://{domain}/{self.short_code}"

    @property
    def is_expired(self):
        """Check if QR code is expired."""
        if not self.expires_at:
            return False
        from django.utils import timezone
        return timezone.now() > self.expires_at

    def increment_scan(self, is_unique=False):
        """Increment scan counters."""
        from django.utils import timezone
        self.total_scans += 1
        if is_unique:
            self.unique_scans += 1
        self.last_scanned_at = timezone.now()
        self.save(update_fields=['total_scans', 'unique_scans', 'last_scanned_at'])


class QRTemplate(models.Model):
    """Pre-designed QR code templates."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    qr_type = models.CharField(max_length=20, choices=QRCode.QR_TYPE_CHOICES)

    # Design presets
    foreground_color = models.CharField(max_length=7, default='#000000')
    background_color = models.CharField(max_length=7, default='#FFFFFF')
    template_image = models.ImageField(upload_to='qr_templates/', blank=True)

    # Settings
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-usage_count', 'name']

    def __str__(self):
        return self.name
