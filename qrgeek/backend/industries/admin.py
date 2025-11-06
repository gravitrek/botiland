"""
Admin configuration for industries app.
"""
from django.contrib import admin
from .models import RestaurantMenu, VCard, WiFiCredentials, EventInfo


@admin.register(RestaurantMenu)
class RestaurantMenuAdmin(admin.ModelAdmin):
    list_display = ['restaurant_name', 'qr_code', 'language', 'created_at']
    search_fields = ['restaurant_name']


@admin.register(VCard)
class VCardAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'email', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'company']


@admin.register(WiFiCredentials)
class WiFiCredentialsAdmin(admin.ModelAdmin):
    list_display = ['ssid', 'security_type', 'hidden', 'created_at']
    list_filter = ['security_type', 'hidden']


@admin.register(EventInfo)
class EventInfoAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date', 'location', 'created_at']
    list_filter = ['event_date']
    search_fields = ['event_name', 'location']
