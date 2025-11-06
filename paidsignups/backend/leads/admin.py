from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['form', 'user', 'status', 'email_sent', 'created_at']
    list_filter = ['status', 'email_sent', 'created_at']
    search_fields = ['user__email', 'form__name', 'data']
    ordering = ['-created_at']
    readonly_fields = ['id', 'email_sent', 'email_sent_at', 'created_at', 'updated_at']
