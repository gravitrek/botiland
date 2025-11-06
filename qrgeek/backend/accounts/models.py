"""
User and authentication models for QRGeek.
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model with additional fields for QRGeek platform.
    """
    INDUSTRY_CHOICES = [
        ('restaurant', 'Restaurant & Food Service'),
        ('retail', 'Retail & E-commerce'),
        ('events', 'Events & Entertainment'),
        ('healthcare', 'Healthcare'),
        ('real_estate', 'Real Estate'),
        ('education', 'Education'),
        ('marketing', 'Marketing & Advertising'),
        ('manufacturing', 'Manufacturing'),
        ('hospitality', 'Hospitality & Tourism'),
        ('nonprofit', 'Non-profit'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=255, blank=True)
    company_name = models.CharField(_('company name'), max_length=255, blank=True)
    industry = models.CharField(
        _('industry'),
        max_length=50,
        choices=INDUSTRY_CHOICES,
        blank=True
    )

    # Email verification
    is_verified = models.BooleanField(_('email verified'), default=False)
    verification_token = models.CharField(max_length=100, blank=True)

    # Subscription
    subscription_plan = models.ForeignKey(
        'SubscriptionPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def qr_code_limit(self):
        """Get QR code limit based on subscription plan."""
        if self.subscription_plan:
            return self.subscription_plan.qr_limit
        return 5  # Free plan default

    @property
    def scan_limit(self):
        """Get monthly scan limit based on subscription plan."""
        if self.subscription_plan:
            return self.subscription_plan.scan_limit
        return 500  # Free plan default

    def has_reached_qr_limit(self):
        """Check if user has reached their QR code creation limit."""
        from qrcodes.models import QRCode
        active_qr_count = QRCode.objects.filter(user=self, is_active=True).count()
        return active_qr_count >= self.qr_code_limit


class SubscriptionPlan(models.Model):
    """
    Subscription plans for QRGeek platform.
    """
    BILLING_PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_period = models.CharField(
        max_length=20,
        choices=BILLING_PERIOD_CHOICES,
        default='monthly'
    )

    # Limits
    qr_limit = models.IntegerField(
        help_text='Maximum number of active QR codes (-1 for unlimited)'
    )
    scan_limit = models.IntegerField(
        help_text='Monthly scan limit (-1 for unlimited)'
    )

    # Features (stored as JSON)
    features = models.JSONField(default=dict, help_text='Plan features as JSON')

    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Order
    display_order = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'price']
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

    def __str__(self):
        return f"{self.name} - ${self.price}/{self.billing_period}"


class UserSubscription(models.Model):
    """
    User's active subscription.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('trial', 'Trial'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # Subscription period
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    cancelled_at = models.DateTimeField(null=True, blank=True)

    # Billing
    auto_renew = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=50, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    @property
    def is_active(self):
        """Check if subscription is currently active."""
        from django.utils import timezone
        return (
            self.status == 'active' and
            self.starts_at <= timezone.now() <= self.ends_at
        )
