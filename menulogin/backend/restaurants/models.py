from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid


class Restaurant(models.Model):
    """
    Restaurant model for multi-tenant SaaS platform.
    Each restaurant is a separate tenant with their own menus, orders, etc.
    """

    SUBSCRIPTION_PLANS = (
        ('FREE', 'Free Plan'),
        ('BASIC', 'Basic Plan'),
        ('PROFESSIONAL', 'Professional Plan'),
        ('ENTERPRISE', 'Enterprise Plan'),
    )

    SUBSCRIPTION_STATUS = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
        ('CANCELLED', 'Cancelled'),
        ('TRIAL', 'Trial'),
    )

    RESTAURANT_TYPES = (
        ('FINE_DINING', 'Fine Dining'),
        ('CASUAL_DINING', 'Casual Dining'),
        ('FAST_FOOD', 'Fast Food'),
        ('CAFE', 'Café'),
        ('BAR', 'Bar/Pub'),
        ('BAKERY', 'Bakery'),
        ('FOOD_TRUCK', 'Food Truck'),
        ('CLOUD_KITCHEN', 'Cloud Kitchen'),
        ('OTHER', 'Other'),
    )

    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    restaurant_type = models.CharField(max_length=20, choices=RESTAURANT_TYPES, default='CASUAL_DINING')

    # Owner
    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='owned_restaurants',
        limit_choices_to={'role__in': ['RESTAURANT_OWNER', 'PLATFORM_ADMIN']}
    )

    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)

    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Images
    logo = models.ImageField(upload_to='restaurants/logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='restaurants/covers/', blank=True, null=True)

    # Operating Hours (JSON field to store schedule)
    operating_hours = models.JSONField(
        default=dict,
        blank=True,
        help_text="Operating hours for each day of the week"
    )

    # Features & Settings
    accepts_dine_in = models.BooleanField(default=True)
    accepts_takeout = models.BooleanField(default=True)
    accepts_delivery = models.BooleanField(default=False)
    accepts_reservations = models.BooleanField(default=False)

    # Payment Settings
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Tax rate in percentage")
    service_charge = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Service charge in percentage")
    accepts_cash = models.BooleanField(default=True)
    accepts_cards = models.BooleanField(default=True)
    accepts_mobile_payment = models.BooleanField(default=False)

    # Subscription & Billing
    subscription_plan = models.CharField(max_length=20, choices=SUBSCRIPTION_PLANS, default='FREE')
    subscription_status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='TRIAL')
    subscription_start_date = models.DateField(blank=True, null=True)
    subscription_end_date = models.DateField(blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata
    settings = models.JSONField(default=dict, blank=True, help_text="Additional settings")

    class Meta:
        db_table = 'restaurants'
        verbose_name = _('Restaurant')
        verbose_name_plural = _('Restaurants')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['subscription_status']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure unique slug
            counter = 1
            original_slug = self.slug
            while Restaurant.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def full_address(self):
        """Return formatted full address."""
        parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, parts))

    def is_subscription_active(self):
        """Check if restaurant has an active subscription."""
        return self.subscription_status in ['ACTIVE', 'TRIAL']


class RestaurantSettings(models.Model):
    """
    Additional restaurant settings and preferences.
    """
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='detailed_settings')

    # Notification Settings
    email_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=False)

    # Order Settings
    auto_accept_orders = models.BooleanField(default=False)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_prep_time = models.IntegerField(default=30, help_text="Average preparation time in minutes")

    # Delivery Settings
    delivery_radius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Delivery radius in km")
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    free_delivery_above = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Table Settings
    total_tables = models.IntegerField(default=0)
    enable_table_qr = models.BooleanField(default=True)

    # Currency & Localization
    currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurant_settings'
        verbose_name = _('Restaurant Settings')
        verbose_name_plural = _('Restaurant Settings')

    def __str__(self):
        return f"Settings for {self.restaurant.name}"
