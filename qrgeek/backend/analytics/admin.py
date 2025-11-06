"""
Admin configuration for analytics app.
"""
from django.contrib import admin
from .models import QRScan, QRAnalytics


@admin.register(QRScan)
class QRScanAdmin(admin.ModelAdmin):
    list_display = ['qr_code', 'scanned_at', 'country', 'city', 'device_type', 'browser']
    list_filter = ['scanned_at', 'country', 'device_type', 'browser']
    search_fields = ['qr_code__name', 'ip_address']
    date_hierarchy = 'scanned_at'
    readonly_fields = ['scanned_at']


@admin.register(QRAnalytics)
class QRAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['qr_code', 'date', 'total_scans', 'unique_scans']
    list_filter = ['date']
    search_fields = ['qr_code__name']
    date_hierarchy = 'date'
