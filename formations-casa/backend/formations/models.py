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


class OnlineFormation(models.Model):
    """Online formation that can be accessed via credits"""
    ACCESS_TYPES = [
        ('free', 'Free'),
        ('credit', 'Credit-based'),
        ('subscription', 'Subscription Only'),
    ]

    MODULE_ACCESS = [
        ('sequential', 'Sequential - Must complete in order'),
        ('flexible', 'Flexible - Access any module'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    short_description = models.TextField(max_length=500)

    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='online_formations')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='online_formations')
    level = models.CharField(max_length=20, choices=Formation.LEVEL_CHOICES, default='all')

    cover_image = models.ImageField(upload_to='online_formations/', null=True, blank=True)
    promo_video_url = models.URLField(blank=True)

    # Access & Pricing
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPES, default='credit')
    credit_cost = models.IntegerField(default=0, help_text="Credits required to access")
    module_access_type = models.CharField(max_length=20, choices=MODULE_ACCESS, default='flexible')

    # Platform Revenue
    platform_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20.00,
        help_text="Platform commission percentage (default from settings)"
    )

    # Stats
    total_enrolled = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class OnlineFormationModule(models.Model):
    """Modules within an online formation"""
    online_formation = models.ForeignKey(OnlineFormation, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = RichTextField()
    order = models.IntegerField(default=0)

    # Prerequisites
    requires_previous_module = models.BooleanField(default=True, help_text="Must complete previous module first")

    estimated_duration_minutes = models.IntegerField(default=60)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ['online_formation', 'order']

    def __str__(self):
        return f"{self.online_formation.title} - Module {self.order}: {self.title}"


class Lesson(models.Model):
    """Individual lessons within a module"""
    LESSON_TYPES = [
        ('video', 'Video'),
        ('article', 'Article/Text'),
        ('pdf', 'PDF Document'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('live', 'Live Session'),
        ('external', 'External Link'),
    ]

    module = models.ForeignKey(OnlineFormationModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True)
    order = models.IntegerField(default=0)

    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='article')

    # Content
    content = RichTextField(blank=True, help_text="For article-type lessons")
    video_url = models.URLField(blank=True, help_text="YouTube, Vimeo, etc.")
    video_duration_minutes = models.IntegerField(default=0)

    # File attachments
    pdf_file = models.FileField(upload_to='lessons/pdfs/', blank=True, null=True)
    attachment = models.FileField(upload_to='lessons/attachments/', blank=True, null=True)

    # External resources
    external_url = models.URLField(blank=True)

    # Settings
    is_downloadable = models.BooleanField(default=False, help_text="Allow downloading attachments")
    is_preview = models.BooleanField(default=False, help_text="Free preview lesson")
    requires_previous_lesson = models.BooleanField(default=True)

    estimated_duration_minutes = models.IntegerField(default=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'order']

    def __str__(self):
        return f"{self.module.title} - Lesson {self.order}: {self.title}"


class OnlineFormationEnrollment(models.Model):
    """Track user enrollments in online formations"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='online_enrollments')
    online_formation = models.ForeignKey(OnlineFormation, on_delete=models.CASCADE, related_name='enrollments')

    # Payment
    credits_paid = models.IntegerField(default=0)
    payment_date = models.DateTimeField(auto_now_add=True)

    # Progress tracking
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    last_accessed = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    # Certificate
    certificate_issued = models.BooleanField(default=False)
    certificate_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'online_formation']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.online_formation.title}"


class LessonProgress(models.Model):
    """Track user progress through lessons"""
    enrollment = models.ForeignKey(OnlineFormationEnrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')

    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    marked_as_studied = models.BooleanField(default=False)

    time_spent_minutes = models.IntegerField(default=0)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['enrollment', 'lesson']
        ordering = ['lesson__order']

    def __str__(self):
        return f"{self.enrollment.user.username} - {self.lesson.title}"


class Quiz(models.Model):
    """Quiz/Test system"""
    VISIBILITY_CHOICES = [
        ('private', 'Private - Only Me'),
        ('public', 'Public - Anyone'),
        ('formation', 'Formation Subscribers Only'),
        ('enrolled', 'My Students Only'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField(blank=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_quizzes')
    online_formation = models.ForeignKey(
        OnlineFormation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quizzes',
        help_text="Optional: Link to online formation"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quizzes',
        help_text="Optional: Link to specific lesson"
    )

    # Settings
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=70.0, help_text="Percentage required to pass")
    time_limit_minutes = models.IntegerField(default=0, help_text="0 = No time limit")
    max_attempts = models.IntegerField(default=0, help_text="0 = Unlimited attempts")

    # Display settings
    show_correct_answers = models.BooleanField(default=True, help_text="Show correct answers after completion")
    randomize_questions = models.BooleanField(default=False)
    randomize_answers = models.BooleanField(default=True)

    # Stats
    total_attempts = models.IntegerField(default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    """Questions for quizzes"""
    QUESTION_TYPES = [
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = RichTextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='single')

    # Multimedia support
    image = models.ImageField(upload_to='quiz_questions/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="Optional video for question")

    order = models.IntegerField(default=0)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)

    explanation = RichTextField(blank=True, help_text="Explanation shown after answering")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class QuizAnswer(models.Model):
    """Answer choices for quiz questions"""
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.question.quiz.title} - Q{self.question.order} - A{self.order}"


class QuizAttempt(models.Model):
    """Track quiz attempts by users"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')

    # Scoring
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    passed = models.BooleanField(default=False)

    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken_minutes = models.IntegerField(default=0)

    # Attempt number for this user
    attempt_number = models.IntegerField(default=1)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} (Attempt {self.attempt_number})"


class QuizResponse(models.Model):
    """Individual question responses within an attempt"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_answers = models.ManyToManyField(QuizAnswer, related_name='user_responses')

    is_correct = models.BooleanField(default=False)
    points_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question}"


# ========== ADDITIONAL CREATIVE FEATURES ==========

# 1. CERTIFICATE SYSTEM
class Certificate(models.Model):
    """Digital certificates for completed formations"""
    CERTIFICATE_TYPES = [
        ('completion', 'Certificate of Completion'),
        ('achievement', 'Certificate of Achievement'),
        ('excellence', 'Certificate of Excellence'),
        ('participation', 'Certificate of Participation'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    online_formation = models.ForeignKey(
        OnlineFormation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='certificates'
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='certificates'
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='certificates'
    )

    certificate_type = models.CharField(max_length=20, choices=CERTIFICATE_TYPES, default='completion')

    # Unique verification code (blockchain-style)
    verification_code = models.CharField(max_length=64, unique=True, db_index=True)

    # Certificate details
    title = models.CharField(max_length=200)
    description = models.TextField()
    grade = models.CharField(max_length=10, blank=True, help_text="A+, A, B+, etc.")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Instructor signature
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='issued_certificates'
    )

    # Skills earned
    skills = models.TextField(blank=True, help_text="Comma-separated skills")

    # PDF generation
    certificate_pdf = models.FileField(upload_to='certificates/', blank=True, null=True)

    # Verification
    is_verified = models.BooleanField(default=True)
    verification_url = models.URLField(blank=True)

    # Metadata
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Null = never expires")

    # Sharing
    is_public = models.BooleanField(default=False, help_text="Show on public profile")
    share_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.verification_code:
            import hashlib
            import uuid
            # Generate unique verification code
            unique_string = f"{self.user.id}{uuid.uuid4()}{self.issued_at}"
            self.verification_code = hashlib.sha256(unique_string.encode()).hexdigest()
        super().save(*args, **kwargs)


class CertificateVerification(models.Model):
    """Track certificate verifications"""
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='verifications')
    verified_by_ip = models.GenericIPAddressField()
    verified_at = models.DateTimeField(auto_now_add=True)
    verifier_email = models.EmailField(blank=True)
    verifier_organization = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-verified_at']

    def __str__(self):
        return f"Verification of {self.certificate.verification_code}"


# 2. LIVE STREAMING SYSTEM
class LiveStream(models.Model):
    """Live video streaming for classes and webinars"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live Now'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()

    # Host info
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_streams')
    co_hosts = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='co_hosted_streams', blank=True)

    # Related formations
    online_formation = models.ForeignKey(
        OnlineFormation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='live_streams'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='live_streams'
    )

    # Cover media
    cover_image = models.ImageField(upload_to='livestreams/', blank=True, null=True)

    # Streaming details
    stream_url = models.URLField(blank=True, help_text="RTMP or HLS stream URL")
    stream_key = models.CharField(max_length=200, blank=True)
    chat_enabled = models.BooleanField(default=True)
    recording_enabled = models.BooleanField(default=True)
    recording_url = models.URLField(blank=True, help_text="Recording playback URL")

    # Access control
    is_public = models.BooleanField(default=True)
    requires_enrollment = models.BooleanField(default=False)
    credit_cost = models.IntegerField(default=0, help_text="Credits to attend")
    max_viewers = models.IntegerField(default=1000)

    # Schedule
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)

    # Stats
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    current_viewers = models.IntegerField(default=0)
    peak_viewers = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)

    # Interactive features
    allow_questions = models.BooleanField(default=True)
    allow_polls = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_start']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class LiveStreamAttendance(models.Model):
    """Track who attends live streams"""
    stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE, related_name='attendances')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stream_attendances')

    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    watch_duration_minutes = models.IntegerField(default=0)

    # Engagement
    asked_questions = models.IntegerField(default=0)
    reactions_sent = models.IntegerField(default=0)

    # Certificate eligibility
    eligible_for_certificate = models.BooleanField(default=False)

    class Meta:
        unique_together = ['stream', 'user']
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} - {self.stream.title}"


class LiveStreamMessage(models.Model):
    """Chat messages during live streams"""
    MESSAGE_TYPES = [
        ('chat', 'Chat Message'),
        ('question', 'Question'),
        ('announcement', 'Announcement'),
        ('poll', 'Poll'),
    ]

    stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stream_messages')

    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='chat')
    content = models.TextField()

    # Moderation
    is_pinned = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='answered_questions'
    )

    # Engagement
    reactions = models.JSONField(default=dict, help_text="{'like': 5, 'love': 2}")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"


# 3. AI CONTENT RECOMMENDATION ENGINE
class UserInteraction(models.Model):
    """Track user interactions for AI recommendations"""
    INTERACTION_TYPES = [
        ('view', 'Viewed'),
        ('click', 'Clicked'),
        ('enroll', 'Enrolled'),
        ('complete', 'Completed'),
        ('rate', 'Rated'),
        ('share', 'Shared'),
        ('bookmark', 'Bookmarked'),
        ('search', 'Searched'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interactions')

    # Interaction details
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)

    # Related objects
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True)
    online_formation = models.ForeignKey(OnlineFormation, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    # Search queries
    search_query = models.CharField(max_length=200, blank=True)

    # Context
    duration_seconds = models.IntegerField(default=0, help_text="Time spent on page")
    rating = models.IntegerField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type}"


class ContentRecommendation(models.Model):
    """AI-generated content recommendations"""
    RECOMMENDATION_REASONS = [
        ('popular', 'Popular Right Now'),
        ('trending', 'Trending in Your Area'),
        ('similar', 'Similar to What You Viewed'),
        ('category', 'Based on Your Interests'),
        ('completion', 'Continue Your Learning'),
        ('level', 'Matches Your Level'),
        ('coach', 'From Coaches You Follow'),
        ('ai', 'AI Personalized Pick'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')

    # Recommended content
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True)
    online_formation = models.ForeignKey(OnlineFormation, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)

    # Recommendation details
    reason = models.CharField(max_length=20, choices=RECOMMENDATION_REASONS, default='ai')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, default=0.5, help_text="0-1 confidence")

    # Performance tracking
    shown = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    enrolled = models.BooleanField(default=False)

    shown_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)

    # AI model version
    model_version = models.CharField(max_length=20, default='v1.0')

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="Recommendation expires after 7 days")

    class Meta:
        ordering = ['-confidence_score', '-created_at']
        indexes = [
            models.Index(fields=['user', 'shown', 'expires_at']),
        ]

    def __str__(self):
        content_type = 'Formation' if self.formation else ('Online Formation' if self.online_formation else 'Quiz')
        return f"Recommendation for {self.user.username} - {content_type}"


class UserPreference(models.Model):
    """Store user preferences for better recommendations"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')

    # Preferred categories
    favorite_categories = models.ManyToManyField(Category, related_name='favorited_by', blank=True)

    # Learning preferences
    preferred_level = models.CharField(max_length=20, choices=Formation.LEVEL_CHOICES, blank=True)
    preferred_delivery = models.CharField(max_length=20, choices=Formation.DELIVERY_MODES, blank=True)
    preferred_language = models.CharField(max_length=10, default='fr')

    # Goals
    learning_goals = models.TextField(blank=True)
    weekly_learning_hours = models.IntegerField(default=5)

    # Notifications
    email_recommendations = models.BooleanField(default=True)
    recommendation_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        default='weekly'
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
