from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User model with roles and profile information"""

    ROLE_CHOICES = [
        ('user', 'Regular User'),
        ('coach', 'Coach'),
        ('center', 'Training Center'),
        ('admin', 'Administrator'),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Approval system
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users'
    )

    # Credits system
    credits = models.IntegerField(default=0)

    # Gamification
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    # Location (especially for coaches and centers in Casablanca)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default='Casablanca')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class CoachProfile(models.Model):
    """Extended profile for coaches"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coach_profile')
    specializations = models.TextField(help_text="Comma-separated specializations")
    years_experience = models.IntegerField(default=0)
    certifications = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Bank details for payments
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=100, blank=True)
    bank_rib = models.CharField(max_length=24, blank=True, help_text="RIB for Moroccan banks")

    # Stats
    total_formations = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Coach: {self.user.username}"


class TrainingCenterProfile(models.Model):
    """Extended profile for training centers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='center_profile')
    center_name = models.CharField(max_length=200)
    description = models.TextField()

    # Location details
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Contact
    website = models.URLField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    # Amenities
    has_parking = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_cafe = models.BooleanField(default=False)
    has_accessibility = models.BooleanField(default=False)

    # Stats
    total_rooms = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.center_name
