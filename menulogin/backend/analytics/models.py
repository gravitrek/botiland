from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class DailySalesReport(models.Model):
    """
    Daily sales analytics for restaurants
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='daily_sales')
    date = models.DateField()

    # Order Statistics
    total_orders = models.IntegerField(default=0)
    dine_in_orders = models.IntegerField(default=0)
    takeout_orders = models.IntegerField(default=0)
    delivery_orders = models.IntegerField(default=0)
    cancelled_orders = models.IntegerField(default=0)

    # Revenue
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tips_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discounts_given = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Average Metrics
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_preparation_time = models.IntegerField(default=0, help_text="In minutes")

    # Customer Metrics
    unique_customers = models.IntegerField(default=0)
    new_customers = models.IntegerField(default=0)
    returning_customers = models.IntegerField(default=0)

    # Peak Hours (JSON field storing hourly breakdown)
    hourly_breakdown = models.JSONField(default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_sales_reports'
        verbose_name = _('Daily Sales Report')
        verbose_name_plural = _('Daily Sales Reports')
        unique_together = ['restaurant', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class MenuItemAnalytics(models.Model):
    """
    Analytics for individual menu items
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu_item = models.ForeignKey('menus.MenuItem', on_delete=models.CASCADE, related_name='analytics')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='menu_analytics')
    date = models.DateField()

    # Sales Metrics
    times_ordered = models.IntegerField(default=0)
    quantity_sold = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Cost Analysis
    cost_of_goods = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu_item_analytics'
        verbose_name = _('Menu Item Analytics')
        verbose_name_plural = _('Menu Item Analytics')
        unique_together = ['menu_item', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.menu_item.name} - {self.date}"


class CustomerBehavior(models.Model):
    """
    Track customer behavior patterns for insights
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='behavior_data')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='customer_behaviors')

    # Ordering Patterns
    preferred_order_type = models.CharField(max_length=20, blank=True, null=True)
    preferred_time_slot = models.CharField(max_length=50, blank=True, null=True)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_frequency = models.IntegerField(default=0, help_text="Orders per month")

    # Preferences
    top_categories = models.JSONField(default=list, blank=True)
    top_items = models.JSONField(default=list, blank=True)

    # Engagement
    last_order_date = models.DateField(null=True, blank=True)
    days_since_last_order = models.IntegerField(default=0)
    is_at_risk = models.BooleanField(default=False, help_text="Customer hasn't ordered in a while")

    # Lifetime Value
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer_behaviors'
        verbose_name = _('Customer Behavior')
        verbose_name_plural = _('Customer Behaviors')
        unique_together = ['customer', 'restaurant']

    def __str__(self):
        return f"Behavior data for {self.customer.user.full_name}"
