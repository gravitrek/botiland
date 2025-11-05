from django.db import models
from django.conf import settings


class TrainingCenter(models.Model):
    """Training centers in Casablanca"""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_centers"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    # Location
    address = models.TextField()
    city = models.CharField(max_length=100, default="Casablanca")
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    # Contact
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)

    # Amenities
    has_parking = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_cafe = models.BooleanField(default=False)
    has_accessibility = models.BooleanField(default=False)
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)
    has_computers = models.BooleanField(default=False)

    # Images
    main_image = models.ImageField(upload_to="centers/", null=True, blank=True)

    # Approval
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    # Stats
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    """Rooms within training centers"""

    training_center = models.ForeignKey(
        TrainingCenter, on_delete=models.CASCADE, related_name="rooms"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Capacity and layout
    capacity = models.IntegerField(help_text="Maximum number of people")
    layout_type = models.CharField(
        max_length=50,
        choices=[
            ("classroom", "Classroom Style"),
            ("theater", "Theater Style"),
            ("u_shape", "U-Shape"),
            ("boardroom", "Boardroom"),
            ("workshop", "Workshop"),
        ],
        default="classroom",
    )

    # Dimensions
    area_sqm = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    # Equipment
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)
    has_audio_system = models.BooleanField(default=False)
    has_video_conferencing = models.BooleanField(default=False)
    has_computers = models.BooleanField(default=False)
    computer_count = models.IntegerField(default=0)

    # Pricing
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    daily_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(max_length=3, default="MAD")

    # Status
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.training_center.name} - {self.name}"


class RoomImage(models.Model):
    """Additional images for rooms"""

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="rooms/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]


class RoomAvailability(models.Model):
    """Track availability of rooms"""

    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="availability_slots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    booking = models.ForeignKey(
        "bookings.Booking",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="room_slots",
    )

    class Meta:
        ordering = ["date", "start_time"]
        unique_together = ["room", "date", "start_time"]

    def __str__(self):
        return f"{self.room} - {self.date} {self.start_time}-{self.end_time}"


class CenterReview(models.Model):
    """Reviews for training centers"""

    center = models.ForeignKey(
        TrainingCenter, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="center_reviews",
    )
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["center", "user"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.center.name} ({self.rating}★)"
