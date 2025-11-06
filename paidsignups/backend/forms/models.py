from django.db import models
from django.conf import settings
import uuid


class Form(models.Model):
    """Lead generation form model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forms')

    # Basic info
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)

    # Form configuration (stored as JSON)
    fields = models.JSONField(default=list, help_text="Form fields configuration")
    # Example structure: [
    #     {
    #         "name": "email",
    #         "type": "email",
    #         "label": "Email Address",
    #         "required": true,
    #         "placeholder": "Enter your email",
    #         "validation": {...}
    #     }
    # ]

    # Submission settings
    submit_button_text = models.CharField(max_length=100, default='Submit')
    success_message = models.TextField(default='Thank you for your submission!')
    redirect_url = models.URLField(blank=True, null=True)

    # Email notifications
    send_notification = models.BooleanField(default=True)
    notification_email = models.EmailField(blank=True, null=True)
    notification_subject = models.CharField(max_length=255, default='New Lead Submission')

    # Styling
    theme = models.JSONField(default=dict, help_text="Form theme and styling")

    # Status
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    # Analytics
    views = models.IntegerField(default=0)
    submissions = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    class Meta:
        verbose_name = 'Form'
        verbose_name_plural = 'Forms'
        ordering = ['-created_at']
        unique_together = ['user', 'slug']
