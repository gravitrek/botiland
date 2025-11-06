"""
Industry-specific models for QRGeek.
"""
import uuid
from django.db import models
from django.conf import settings


class RestaurantMenu(models.Model):
    """Restaurant digital menu."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.OneToOneField(
        'qrcodes.QRCode',
        on_delete=models.CASCADE,
        related_name='restaurant_menu'
    )
    restaurant_name = models.CharField(max_length=255)
    menu_data = models.JSONField(help_text='Menu categories, items, prices')
    allergen_info = models.JSONField(default=dict)
    language = models.CharField(max_length=10, default='en')
    theme = models.CharField(max_length=50, default='classic')
    show_prices = models.BooleanField(default=True)
    show_images = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name


class VCard(models.Model):
    """Digital business card."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.OneToOneField(
        'qrcodes.QRCode',
        on_delete=models.CASCADE,
        related_name='vcard'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    social_links = models.JSONField(default=dict)
    photo = models.ImageField(upload_to='vcards/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class WiFiCredentials(models.Model):
    """WiFi access credentials."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.OneToOneField(
        'qrcodes.QRCode',
        on_delete=models.CASCADE,
        related_name='wifi'
    )
    ssid = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    security_type = models.CharField(
        max_length=10,
        choices=[('WPA', 'WPA/WPA2'), ('WEP', 'WEP'), ('', 'None')],
        default='WPA'
    )
    hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WiFi: {self.ssid}"


class EventInfo(models.Model):
    """Event information."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.OneToOneField(
        'qrcodes.QRCode',
        on_delete=models.CASCADE,
        related_name='event'
    )
    event_name = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    ticket_info = models.JSONField(default=dict)
    registration_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name
