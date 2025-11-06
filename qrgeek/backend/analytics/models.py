"""
Analytics and tracking models.
"""
import uuid
from django.db import models


class QRScan(models.Model):
    """Individual QR code scan record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.ForeignKey(
        'qrcodes.QRCode',
        on_delete=models.CASCADE,
        related_name='scans'
    )
    scanned_at = models.DateTimeField(auto_now_add=True)

    # Location
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Device info
    device_type = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    user_agent = models.TextField(blank=True)

    # Referer
    referer = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['-scanned_at']
        indexes = [
            models.Index(fields=['qr_code', '-scanned_at']),
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        return f"Scan of {self.qr_code.name} at {self.scanned_at}"


class QRAnalytics(models.Model):
    """Aggregated daily analytics for QR codes."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.ForeignKey(
        'qrcodes.QRCode',
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    date = models.DateField()

    # Aggregated stats
    total_scans = models.IntegerField(default=0)
    unique_scans = models.IntegerField(default=0)
    top_countries = models.JSONField(default=dict)
    top_cities = models.JSONField(default=dict)
    top_devices = models.JSONField(default=dict)
    top_browsers = models.JSONField(default=dict)
    top_os = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['qr_code', 'date']
        ordering = ['-date']
        verbose_name_plural = 'QR Analytics'

    def __str__(self):
        return f"{self.qr_code.name} - {self.date}"
