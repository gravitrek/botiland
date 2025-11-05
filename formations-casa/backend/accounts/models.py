from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User model with roles and profile information"""

    ROLE_CHOICES = [
        ('user', 'Regular User'),
        ('coach', 'Coach'),
        ('center', 'Training Center'),
        ('admin', 'Administrator'),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Approval system - deprecated, now auto-approved
    is_approved = models.BooleanField(default=True, help_text="Auto-approved - legacy field")
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users'
    )

    # Verified badge system - replaced approval
    is_verified = models.BooleanField(default=False, help_text="Has verified badge")
    verification_requested = models.BooleanField(default=False)
    verification_requested_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_users'
    )

    # Credits system
    credits = models.IntegerField(default=0)

    # Gamification
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    # Location (especially for coaches and centers in Casablanca)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default='Casablanca')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class CoachProfile(models.Model):
    """Extended profile for coaches"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coach_profile')
    specializations = models.TextField(help_text="Comma-separated specializations")
    years_experience = models.IntegerField(default=0)
    certifications = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Bank details for payments
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=100, blank=True)
    bank_rib = models.CharField(max_length=24, blank=True, help_text="RIB for Moroccan banks")

    # Stats
    total_formations = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Coach: {self.user.username}"


class TrainingCenterProfile(models.Model):
    """Extended profile for training centers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='center_profile')
    center_name = models.CharField(max_length=200)
    description = models.TextField()

    # Location details
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Contact
    website = models.URLField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    # Amenities
    has_parking = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_cafe = models.BooleanField(default=False)
    has_accessibility = models.BooleanField(default=False)

    # Stats
    total_rooms = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.center_name


class VerificationRequest(models.Model):
    """Track verification badge requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_requests')

    # Request details
    motivation = models.TextField(help_text="Why user wants verification")
    credentials = models.TextField(blank=True, help_text="Professional credentials, certifications, etc.")
    website = models.URLField(blank=True)
    social_proof = models.URLField(blank=True, help_text="LinkedIn, portfolio, etc.")

    # Document uploads
    id_document = models.FileField(upload_to='verification_docs/', null=True, blank=True)
    credential_document = models.FileField(upload_to='verification_docs/', null=True, blank=True)

    # Credits
    credits_paid = models.IntegerField(default=0, help_text="Credits paid for verification request")

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_verifications'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Verification Request - {self.user.username} ({self.status})"


class PlatformSettings(models.Model):
    """Global platform settings for pricing and configuration"""
    # Credit pricing
    credit_price_mad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1.00,
        help_text="Price of 1 credit in MAD"
    )

    # Feature costs
    verification_badge_cost = models.IntegerField(
        default=100,
        help_text="Credits required for verification badge application"
    )
    featured_formation_cost = models.IntegerField(
        default=50,
        help_text="Credits to feature a formation"
    )
    premium_listing_cost = models.IntegerField(
        default=75,
        help_text="Credits for premium listing"
    )

    # Revenue sharing
    default_platform_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20.00,
        help_text="Default platform commission percentage"
    )

    # Credit packages
    credit_package_small = models.IntegerField(default=10)
    credit_package_small_bonus = models.IntegerField(default=0)

    credit_package_medium = models.IntegerField(default=50)
    credit_package_medium_bonus = models.IntegerField(default=5)

    credit_package_large = models.IntegerField(default=100)
    credit_package_large_bonus = models.IntegerField(default=15)

    credit_package_xl = models.IntegerField(default=500)
    credit_package_xl_bonus = models.IntegerField(default=100)

    # Other settings
    min_withdrawal_credits = models.IntegerField(default=1000, help_text="Minimum credits for coach withdrawal")

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='platform_settings_updates'
    )

    class Meta:
        verbose_name_plural = "Platform Settings"

    def __str__(self):
        return f"Platform Settings (Updated: {self.updated_at})"

    @classmethod
    def get_settings(cls):
        """Get or create platform settings singleton"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings


class CreditTransaction(models.Model):
    """Track all credit transactions"""
    TRANSACTION_TYPES = [
        ('purchase', 'Credit Purchase'),
        ('spent', 'Credits Spent'),
        ('earned', 'Credits Earned'),
        ('refund', 'Credit Refund'),
        ('bonus', 'Bonus Credits'),
        ('admin_adjustment', 'Admin Adjustment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_transactions')

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.IntegerField(help_text="Positive for credits added, negative for spent")
    balance_after = models.IntegerField(help_text="User's credit balance after this transaction")

    # Related objects
    description = models.TextField()
    online_formation = models.ForeignKey(
        'formations.OnlineFormation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    verification_request = models.ForeignKey(
        VerificationRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Payment details for purchases
    payment_amount_mad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount paid in MAD for credit purchase"
    )
    payment_proof = models.FileField(upload_to='credit_payments/', null=True, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('rejected', 'Rejected'),
        ],
        default='confirmed'
    )

    # Admin tracking
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_transactions'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type}: {self.amount} credits"
