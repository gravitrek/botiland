from django.contrib import admin
from .models import LandingPage


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'slug', 'is_published', 'views', 'conversions', 'created_at']
    list_filter = ['is_active', 'is_published', 'created_at']
    search_fields = ['name', 'slug', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['id', 'views', 'conversions', 'created_at', 'updated_at']
