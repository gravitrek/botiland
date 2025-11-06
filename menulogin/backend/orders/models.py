from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Order(models.Model):
    """
    Main Order model for managing customer orders
    """
    ORDER_TYPES = (
        ('DINE_IN', 'Dine In'),
        ('TAKEOUT', 'Takeout'),
        ('DELIVERY', 'Delivery'),
        ('ONLINE', 'Online'),
    )

    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    )

    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='orders')

    # Customer Information
    customer = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20)

    # Order Details
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, default='DINE_IN')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')

    # Table Information (for dine-in orders)
    table = models.ForeignKey('tables.Table', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    table_number = models.CharField(max_length=20, blank=True, null=True)

    # Delivery Information
    delivery_address = models.TextField(blank=True, null=True)
    delivery_city = models.CharField(max_length=100, blank=True, null=True)
    delivery_postal_code = models.CharField(max_length=20, blank=True, null=True)
    delivery_instructions = models.TextField(blank=True, null=True)
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tip_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Discount/Coupon
    coupon_code = models.CharField(max_length=50, blank=True, null=True)

    # Special Instructions
    special_instructions = models.TextField(blank=True, null=True)

    # Timing
    estimated_prep_time = models.IntegerField(default=30, help_text="Estimated preparation time in minutes")
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    scheduled_time = models.DateTimeField(null=True, blank=True, help_text="For scheduled orders")

    # Staff Assignment
    assigned_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders', limit_choices_to={'role__in': ['RESTAURANT_STAFF', 'RESTAURANT_MANAGER']})

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    preparing_at = models.DateTimeField(null=True, blank=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'orders'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['restaurant', 'order_status']),
            models.Index(fields=['order_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Order {self.order_number} - {self.restaurant.name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            import random
            import string
            while True:
                order_num = f"ORD-{''.join(random.choices(string.digits, k=8))}"
                if not Order.objects.filter(order_number=order_num).exists():
                    self.order_number = order_num
                    break
        super().save(*args, **kwargs)

    def calculate_totals(self):
        """Calculate order totals based on items."""
        self.subtotal = sum(item.total_price for item in self.items.all())

        # Calculate tax
        if self.restaurant.tax_rate:
            self.tax_amount = (self.subtotal * self.restaurant.tax_rate) / 100

        # Calculate service charge
        if self.restaurant.service_charge:
            self.service_charge = (self.subtotal * self.restaurant.service_charge) / 100

        # Calculate total
        self.total_amount = (
            self.subtotal +
            self.tax_amount +
            self.service_charge +
            self.delivery_fee +
            self.tip_amount -
            self.discount_amount
        )
        self.save()


class OrderItem(models.Model):
    """
    Individual items in an order
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('menus.MenuItem', on_delete=models.PROTECT, related_name='order_items')

    # Item Details (stored to preserve order history even if menu changes)
    item_name = models.CharField(max_length=200)
    item_description = models.TextField(blank=True, null=True)

    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Variant (if applicable)
    variant = models.ForeignKey('menus.MenuItemVariant', on_delete=models.SET_NULL, null=True, blank=True)
    variant_name = models.CharField(max_length=100, blank=True, null=True)

    # Special Instructions
    special_instructions = models.TextField(blank=True, null=True)

    # Status
    is_prepared = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.quantity}x {self.item_name}"

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class OrderItemModifier(models.Model):
    """
    Modifiers selected for order items
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='modifiers')
    modifier_name = models.CharField(max_length=100)
    option_name = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_item_modifiers'
        verbose_name = _('Order Item Modifier')
        verbose_name_plural = _('Order Item Modifiers')

    def __str__(self):
        return f"{self.modifier_name}: {self.option_name}"


class OrderStatusHistory(models.Model):
    """
    Track order status changes for audit trail
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_status_history'
        verbose_name = _('Order Status History')
        verbose_name_plural = _('Order Status Histories')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.order.order_number}: {self.old_status} → {self.new_status}"
