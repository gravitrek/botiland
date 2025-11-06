from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with subscription and profile information"""

    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Subscription info
    subscription_plan = models.CharField(
        max_length=20,
        choices=[
            ('FREE', 'Free'),
            ('BASIC', 'Basic'),
            ('PRO', 'Pro'),
            ('ENTERPRISE', 'Enterprise'),
        ],
        default='FREE'
    )
    subscription_active = models.BooleanField(default=True)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)

    # PayPal info
    paypal_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_payer_id = models.CharField(max_length=255, blank=True, null=True)

    # Admin fields
    is_verified = models.BooleanField(default=False)

    # Usage tracking
    forms_created = models.IntegerField(default=0)
    landing_pages_created = models.IntegerField(default=0)
    leads_this_month = models.IntegerField(default=0)
    last_lead_reset = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
