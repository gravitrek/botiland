from django.db import models
from django.conf import settings


class Feature(models.Model):
    """Platform features that can be gated by credits/subscription"""

    FEATURE_TYPES = [
        ('formation', 'Formation Related'),
        ('center', 'Training Center Related'),
        ('marketing', 'Marketing & Promotion'),
        ('analytics', 'Analytics & Reporting'),
        ('communication', 'Communication'),
        ('content', 'Content Management'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    feature_type = models.CharField(max_length=20, choices=FEATURE_TYPES)

    # Cost
    credits_cost = models.IntegerField(default=0, help_text="Credits needed to use this feature")

    # Limits
    is_limited = models.BooleanField(default=False)
    usage_limit_per_month = models.IntegerField(null=True, blank=True)

    # Availability
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)

    # Role restrictions
    available_for_users = models.BooleanField(default=True)
    available_for_coaches = models.BooleanField(default=True)
    available_for_centers = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['feature_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.credits_cost} credits)"


class FeatureUsage(models.Model):
    """Track feature usage by users"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feature_usage')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='usage_records')

    # Usage details
    credits_spent = models.IntegerField()
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional usage data")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.feature.name}"


class CreditPurchase(models.Model):
    """Track credit purchases by users"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_purchases')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credits = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Payment details
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_proof = models.ImageField(upload_to='credit_purchases/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.credits} credits ({self.amount} MAD)"


class Subscription(models.Model):
    """Subscription plans for enhanced features"""

    PLAN_TYPES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)

    # Credits
    monthly_credits = models.IntegerField(default=0)

    # Dates
    start_date = models.DateField()
    end_date = models.DateField()

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    auto_renew = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_plan_type_display()} ({self.status})"
