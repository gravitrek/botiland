from django.contrib import admin
from .models import Form


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'slug', 'is_published', 'views', 'submissions', 'created_at']
    list_filter = ['is_active', 'is_published', 'created_at']
    search_fields = ['name', 'slug', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['id', 'views', 'submissions', 'created_at', 'updated_at']
