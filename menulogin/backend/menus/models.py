from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
import uuid


class MenuCategory(models.Model):
    """
    Menu categories for organizing menu items (e.g., Appetizers, Main Course, Desserts)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='menu_categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='menu/categories/', blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu_categories'
        verbose_name = _('Menu Category')
        verbose_name_plural = _('Menu Categories')
        ordering = ['display_order', 'name']
        unique_together = ['restaurant', 'name']

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class MenuItem(models.Model):
    """
    Individual menu items/dishes
    """
    DIETARY_TYPES = (
        ('NONE', 'None'),
        ('VEGETARIAN', 'Vegetarian'),
        ('VEGAN', 'Vegan'),
        ('GLUTEN_FREE', 'Gluten Free'),
        ('DAIRY_FREE', 'Dairy Free'),
        ('HALAL', 'Halal'),
        ('KOSHER', 'Kosher'),
    )

    SPICE_LEVELS = (
        ('NONE', 'None'),
        ('MILD', 'Mild'),
        ('MEDIUM', 'Medium'),
        ('HOT', 'Hot'),
        ('EXTRA_HOT', 'Extra Hot'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')

    # Basic Information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='menu/items/', blank=True, null=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Cost to make this item")

    # Availability
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    # Dietary & Allergen Information
    dietary_type = models.CharField(max_length=20, choices=DIETARY_TYPES, default='NONE')
    spice_level = models.CharField(max_length=20, choices=SPICE_LEVELS, default='NONE')
    allergens = models.JSONField(default=list, blank=True, help_text="List of allergens")
    calories = models.IntegerField(null=True, blank=True)

    # Preparation
    prep_time = models.IntegerField(default=15, help_text="Preparation time in minutes")

    # Inventory
    track_inventory = models.BooleanField(default=False)
    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)

    # Display
    display_order = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'menu_items'
        verbose_name = _('Menu Item')
        verbose_name_plural = _('Menu Items')
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['restaurant', 'is_available']),
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    @property
    def in_stock(self):
        """Check if item is in stock."""
        if not self.track_inventory:
            return True
        return self.stock_quantity > 0

    @property
    def is_low_stock(self):
        """Check if item is low on stock."""
        if not self.track_inventory:
            return False
        return 0 < self.stock_quantity <= self.low_stock_threshold

    def reduce_stock(self, quantity=1):
        """Reduce stock quantity."""
        if self.track_inventory and self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save(update_fields=['stock_quantity'])
            return True
        return False


class MenuItemModifier(models.Model):
    """
    Modifiers for menu items (e.g., Extra Cheese, No Onions, Size variations)
    """
    MODIFIER_TYPES = (
        ('SINGLE', 'Single Choice'),
        ('MULTIPLE', 'Multiple Choice'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='modifiers')
    name = models.CharField(max_length=100, help_text="e.g., Size, Toppings, Extras")
    modifier_type = models.CharField(max_length=20, choices=MODIFIER_TYPES, default='SINGLE')
    is_required = models.BooleanField(default=False)
    min_selections = models.IntegerField(default=0)
    max_selections = models.IntegerField(default=1)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu_item_modifiers'
        verbose_name = _('Menu Item Modifier')
        verbose_name_plural = _('Menu Item Modifiers')
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_modifier_type_display()})"


class MenuItemModifierOption(models.Model):
    """
    Options for modifiers (e.g., Small/Medium/Large for Size modifier)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    modifier = models.ForeignKey(MenuItemModifier, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional price for this option")
    is_default = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu_item_modifier_options'
        verbose_name = _('Modifier Option')
        verbose_name_plural = _('Modifier Options')
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} (+{self.price_adjustment})"


class MenuItemModifierLink(models.Model):
    """
    Links menu items with their available modifiers
    """
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='modifier_links')
    modifier = models.ForeignKey(MenuItemModifier, on_delete=models.CASCADE, related_name='item_links')
    is_required = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu_item_modifier_links'
        unique_together = ['menu_item', 'modifier']
        ordering = ['display_order']

    def __str__(self):
        return f"{self.menu_item.name} - {self.modifier.name}"


class MenuItemVariant(models.Model):
    """
    Variants of menu items (e.g., Sizes, Flavors)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100, help_text="e.g., Small, Medium, Large, Chocolate, Vanilla")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sku = models.CharField(max_length=100, blank=True, null=True, help_text="Stock Keeping Unit")
    is_available = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu_item_variants'
        verbose_name = _('Menu Item Variant')
        verbose_name_plural = _('Menu Item Variants')
        ordering = ['display_order', 'name']
        unique_together = ['menu_item', 'name']

    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"
