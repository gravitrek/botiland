from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Notification(models.Model):
    """
    System notifications for users (email, WhatsApp, in-app)
    """
    NOTIFICATION_TYPES = (
        ('ORDER_RECEIVED', 'Order Received'),
        ('ORDER_CONFIRMED', 'Order Confirmed'),
        ('ORDER_READY', 'Order Ready'),
        ('ORDER_DELIVERED', 'Order Delivered'),
        ('ORDER_CANCELLED', 'Order Cancelled'),
        ('RESERVATION_CONFIRMED', 'Reservation Confirmed'),
        ('RESERVATION_REMINDER', 'Reservation Reminder'),
        ('PAYMENT_RECEIVED', 'Payment Received'),
        ('SUBSCRIPTION_EXPIRING', 'Subscription Expiring'),
        ('SYSTEM_ALERT', 'System Alert'),
    )

    NOTIFICATION_CHANNELS = (
        ('EMAIL', 'Email'),
        ('WHATSAPP', 'WhatsApp'),
        ('SMS', 'SMS'),
        ('IN_APP', 'In-App'),
        ('PUSH', 'Push Notification'),
    )

    NOTIFICATION_STATUS = (
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
        ('READ', 'Read'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')

    # Notification Details
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    channel = models.CharField(max_length=20, choices=NOTIFICATION_CHANNELS)
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS, default='PENDING')

    # Content
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True, help_text="Additional data for the notification")

    # Related Objects
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)

    # Delivery Information
    recipient_email = models.EmailField(blank=True, null=True)
    recipient_phone = models.CharField(max_length=20, blank=True, null=True)

    # Status Tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    failed_reason = models.TextField(blank=True, null=True)

    # Retry Logic
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.notification_type} - {self.user.email} ({self.channel})"


class EmailTemplate(models.Model):
    """
    Email templates for automated notifications
    """
    TEMPLATE_TYPES = (
        ('ORDER_CONFIRMATION', 'Order Confirmation'),
        ('ORDER_READY', 'Order Ready'),
        ('ORDER_DELIVERED', 'Order Delivered'),
        ('RESERVATION_CONFIRMATION', 'Reservation Confirmation'),
        ('PASSWORD_RESET', 'Password Reset'),
        ('WELCOME_EMAIL', 'Welcome Email'),
        ('SUBSCRIPTION_REMINDER', 'Subscription Reminder'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='email_templates', null=True, blank=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=255)
    body_html = models.TextField(help_text="HTML email body")
    body_text = models.TextField(help_text="Plain text email body", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_templates'
        verbose_name = _('Email Template')
        verbose_name_plural = _('Email Templates')

    def __str__(self):
        return f"{self.name} ({self.template_type})"
