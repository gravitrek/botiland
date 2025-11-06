"""
Admin configuration for qrcodes app.
"""
from django.contrib import admin
from .models import QRCode, Tag, QRTemplate


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'user', 'qr_type', 'short_code', 'total_scans',
        'is_active', 'created_at'
    ]
    list_filter = ['qr_type', 'is_active', 'enable_tracking', 'created_at']
    search_fields = ['name', 'short_code', 'user__email']
    readonly_fields = ['short_code', 'total_scans', 'unique_scans', 'last_scanned_at']
    date_hierarchy = 'created_at'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name', 'user__email']


@admin.register(QRTemplate)
class QRTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'qr_type', 'is_premium', 'usage_count', 'is_active']
    list_filter = ['category', 'qr_type', 'is_premium', 'is_active']
    search_fields = ['name', 'description']
