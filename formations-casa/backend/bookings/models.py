from django.db import models
from django.conf import settings


class Booking(models.Model):
    """Bookings/enrollments for formations"""

    STATUS_CHOICES = [
        ("pending", "Pending Confirmation"),
        ("confirmed", "Confirmed"),
        ("payment_pending", "Payment Pending"),
        ("payment_received", "Payment Received"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    # Basic info
    formation = models.ForeignKey(
        "formations.Formation", on_delete=models.CASCADE, related_name="bookings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    booking_code = models.CharField(max_length=20, unique=True)

    # Payment info
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="MAD")
    payment_instructions_sent = models.BooleanField(default=False)
    payment_instructions_sent_at = models.DateTimeField(null=True, blank=True)

    # Notes
    user_notes = models.TextField(blank=True, help_text="Notes from the user")
    admin_notes = models.TextField(blank=True, help_text="Internal notes")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["formation", "user"]

    def __str__(self):
        return f"{self.booking_code} - {self.user.username} - {self.formation.title}"


class BookingNotification(models.Model):
    """Track notifications sent for bookings"""

    NOTIFICATION_TYPES = [
        ("confirmation", "Booking Confirmation"),
        ("payment_instructions", "Payment Instructions"),
        ("payment_received", "Payment Received"),
        ("reminder", "Reminder"),
        ("cancellation", "Cancellation"),
    ]

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.booking.booking_code} - {self.get_notification_type_display()}"


class Attendance(models.Model):
    """Track attendance for bookings"""

    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="attendance"
    )
    attended = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.booking.booking_code} - Attended: {self.attended}"
