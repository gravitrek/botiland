from django.db import models
from django.conf import settings
import uuid


class LandingPage(models.Model):
    """Customizable landing page model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='landing_pages')

    # Basic info
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)

    # Content (stored as JSON - page builder format)
    content = models.JSONField(default=dict, help_text="Landing page content and layout")
    # Example structure: {
    #     "sections": [
    #         {
    #             "type": "hero",
    #             "title": "...",
    #             "subtitle": "...",
    #             "image": "...",
    #             "cta": {...}
    #         },
    #         {
    #             "type": "form",
    #             "form_id": "uuid"
    #         }
    #     ]
    # }

    # Associated form (optional)
    form = models.ForeignKey('forms.Form', on_delete=models.SET_NULL, null=True, blank=True, related_name='landing_pages')

    # SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True)

    # Styling
    theme = models.JSONField(default=dict, help_text="Landing page theme and styling")
    custom_css = models.TextField(blank=True, null=True)
    custom_js = models.TextField(blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    # Analytics
    views = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)

    # Tracking
    tracking_code = models.TextField(blank=True, null=True, help_text="Google Analytics, Facebook Pixel, etc.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    @property
    def conversion_rate(self):
        if self.views == 0:
            return 0
        return (self.conversions / self.views) * 100

    class Meta:
        verbose_name = 'Landing Page'
        verbose_name_plural = 'Landing Pages'
        ordering = ['-created_at']
        unique_together = ['user', 'slug']
