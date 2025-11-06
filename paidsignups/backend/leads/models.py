from django.db import models
from django.conf import settings
import uuid


class Lead(models.Model):
    """Lead/submission from a form"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey('forms.Form', on_delete=models.CASCADE, related_name='leads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leads')

    # Lead data (stored as JSON)
    data = models.JSONField(default=dict, help_text="Form submission data")

    # Source tracking
    source_url = models.URLField(blank=True, null=True)
    source_landing_page = models.ForeignKey(
        'landing_pages.LandingPage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )
    referrer = models.URLField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    # Lead status
    status = models.CharField(
        max_length=20,
        choices=[
            ('NEW', 'New'),
            ('CONTACTED', 'Contacted'),
            ('QUALIFIED', 'Qualified'),
            ('CONVERTED', 'Converted'),
            ('LOST', 'Lost'),
        ],
        default='NEW'
    )
    notes = models.TextField(blank=True, null=True)

    # Email tracking
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead for {self.form.name} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']
