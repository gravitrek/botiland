from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
import qrcode
from io import BytesIO
from django.core.files import File


class Table(models.Model):
    """
    Restaurant table management with QR code support
    """
    TABLE_STATUS = (
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('RESERVED', 'Reserved'),
        ('MAINTENANCE', 'Maintenance'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='tables')
    table_number = models.CharField(max_length=20)
    table_name = models.CharField(max_length=100, blank=True, null=True, help_text="Optional table name (e.g., 'Window Table 1')")

    # Capacity
    capacity = models.IntegerField(default=4, help_text="Number of seats")

    # Location
    floor = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Indoor, Outdoor, VIP")

    # Status
    status = models.CharField(max_length=20, choices=TABLE_STATUS, default='AVAILABLE')
    is_active = models.BooleanField(default=True)

    # QR Code
    qr_code = models.ImageField(upload_to='tables/qr_codes/', blank=True, null=True)
    qr_code_url = models.CharField(max_length=500, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tables'
        verbose_name = _('Table')
        verbose_name_plural = _('Tables')
        unique_together = ['restaurant', 'table_number']
        ordering = ['table_number']

    def __str__(self):
        return f"Table {self.table_number} - {self.restaurant.name}"

    def generate_qr_code(self, base_url):
        """Generate QR code for table ordering."""
        # Create URL for table (e.g., https://menulogin.com/r/restaurant-slug/table/uuid)
        self.qr_code_url = f"{base_url}/r/{self.restaurant.slug}/table/{self.id}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.qr_code_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save to file
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f'table_{self.restaurant.slug}_{self.table_number}_qr.png'
        self.qr_code.save(file_name, File(buffer), save=False)
        buffer.close()

        self.save()

    def get_current_order(self):
        """Get current active order for this table."""
        from orders.models import Order
        return Order.objects.filter(
            table=self,
            order_status__in=['PENDING', 'CONFIRMED', 'PREPARING']
        ).first()


class TableReservation(models.Model):
    """
    Table reservation system
    """
    RESERVATION_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SEATED', 'Seated'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')

    # Customer Information
    customer = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)

    # Reservation Details
    party_size = models.IntegerField(help_text="Number of guests")
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    duration = models.IntegerField(default=120, help_text="Expected duration in minutes")

    # Status
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS, default='PENDING')

    # Special Requests
    special_requests = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    seated_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'table_reservations'
        verbose_name = _('Table Reservation')
        verbose_name_plural = _('Table Reservations')
        ordering = ['reservation_date', 'reservation_time']
        indexes = [
            models.Index(fields=['restaurant', 'reservation_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Reservation for {self.customer_name} on {self.reservation_date} at {self.reservation_time}"


class TableSession(models.Model):
    """
    Track table usage sessions (when customers sit down to when they leave)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='sessions')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='table_sessions')

    # Session Details
    party_size = models.IntegerField(default=1)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Associated order
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='table_session')

    # Staff
    served_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='served_sessions')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'table_sessions'
        verbose_name = _('Table Session')
        verbose_name_plural = _('Table Sessions')
        ordering = ['-start_time']

    def __str__(self):
        return f"Session at {self.table.table_number} - {self.start_time}"

    @property
    def duration_minutes(self):
        """Calculate session duration in minutes."""
        if self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return None
