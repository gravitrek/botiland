from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Customer(models.Model):
    """
    Customer profile with order history and preferences
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='customer_profile')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='customers')

    # Loyalty Program
    loyalty_points = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Preferences
    favorite_items = models.ManyToManyField('menus.MenuItem', blank=True, related_name='favorited_by')
    dietary_preferences = models.JSONField(default=list, blank=True)
    allergen_info = models.JSONField(default=list, blank=True)

    # Address Book
    default_delivery_address = models.TextField(blank=True, null=True)

    # Timestamps
    first_order_date = models.DateTimeField(null=True, blank=True)
    last_order_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Tags
    tags = models.JSONField(default=list, blank=True, help_text="Customer tags (e.g., VIP, Regular)")

    class Meta:
        db_table = 'customers'
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        unique_together = ['user', 'restaurant']

    def __str__(self):
        return f"{self.user.full_name} - {self.restaurant.name}"

    def add_loyalty_points(self, points):
        """Add loyalty points to customer."""
        self.loyalty_points += points
        self.save(update_fields=['loyalty_points'])

    def redeem_loyalty_points(self, points):
        """Redeem loyalty points."""
        if self.loyalty_points >= points:
            self.loyalty_points -= points
            self.save(update_fields=['loyalty_points'])
            return True
        return False


class CustomerAddress(models.Model):
    """
    Customer saved delivery addresses
    """
    ADDRESS_TYPES = (
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('OTHER', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='HOME')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer_addresses'
        verbose_name = _('Customer Address')
        verbose_name_plural = _('Customer Addresses')

    def __str__(self):
        return f"{self.get_address_type_display()} - {self.city}"
