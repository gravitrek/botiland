from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField


class Category(models.Model):
    """Categories for formations"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class FormationType(models.Model):
    """Types of formations (online, in-person, hybrid)"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Formation(models.Model):
    """Main formation/training model"""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    DELIVERY_MODES = [
        ('in_person', 'In Person'),
        ('remote', 'Remote/Online'),
        ('hybrid', 'Hybrid'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all', 'All Levels'),
    ]

    # Basic info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    short_description = models.TextField(max_length=500)

    # Organization
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='formations')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='formations')
    formation_type = models.ForeignKey(FormationType, on_delete=models.SET_NULL, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='all')

    # Media
    cover_image = models.ImageField(upload_to='formations/', null=True, blank=True)
    video_url = models.URLField(blank=True, help_text="Promo video URL")

    # Delivery
    delivery_mode = models.CharField(max_length=20, choices=DELIVERY_MODES, default='in_person')
    training_center = models.ForeignKey(
        'centers.TrainingCenter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='formations'
    )
    room = models.ForeignKey(
        'centers.Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='formations'
    )
    online_platform = models.CharField(max_length=100, blank=True, help_text="e.g., Zoom, Teams")
    meeting_link = models.URLField(blank=True)

    # Schedule
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration_hours = models.DecimalField(max_digits=5, decimal_places=1)

    # Enrollment
    max_participants = models.IntegerField(default=20)
    min_participants = models.IntegerField(default=1)
    current_participants = models.IntegerField(default=0)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='MAD')

    # Requirements
    prerequisites = RichTextField(blank=True)
    required_materials = RichTextField(blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)

    # Stats
    views_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_ratings = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Curriculum(models.Model):
    """Curriculum/syllabus for a formation"""
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='curriculum_items')
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    description = RichTextField()
    duration_minutes = models.IntegerField(default=60)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.formation.title} - {self.title}"


class FormationReview(models.Model):
    """Reviews and ratings for formations"""
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='formation_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['formation', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.formation.title} ({self.rating}★)"
