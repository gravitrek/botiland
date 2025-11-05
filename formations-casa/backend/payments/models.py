from django.db import models
from django.conf import settings


class Payment(models.Model):
    """Payment records for bookings"""

    PAYMENT_METHODS = [
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='MAD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    # Payment details
    transaction_reference = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField()
    proof_of_payment = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)

    # Bank details used for this payment
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=100, blank=True)

    # Verification
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_payments'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} - {self.booking.booking_code} - {self.amount} {self.currency}"


class PaymentInstruction(models.Model):
    """Payment instructions that coaches provide"""
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_instructions'
    )
    formation = models.ForeignKey(
        'formations.Formation',
        on_delete=models.CASCADE,
        related_name='payment_instructions',
        null=True,
        blank=True
    )

    # Bank details
    bank_name = models.CharField(max_length=100)
    bank_account_name = models.CharField(max_length=200)
    bank_account_number = models.CharField(max_length=100)
    bank_rib = models.CharField(max_length=24, blank=True)
    bank_swift = models.CharField(max_length=20, blank=True)

    # Additional instructions
    additional_info = models.TextField(blank=True)

    # If null, applies to all coach's formations
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.formation:
            return f"Payment instructions for {self.formation.title}"
        return f"Default payment instructions for {self.coach.username}"


class Reconciliation(models.Model):
    """Track payment reconciliation by coaches"""
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reconciliations'
    )
    formation = models.ForeignKey('formations.Formation', on_delete=models.CASCADE, related_name='reconciliations')

    # Financial summary
    total_bookings = models.IntegerField(default=0)
    total_expected = models.DecimalField(max_digits=10, decimal_places=2)
    total_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Period
    period_start = models.DateField()
    period_end = models.DateField()

    # Status
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reconciliation: {self.formation.title} ({self.period_start} to {self.period_end})"
