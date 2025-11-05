from django.contrib import admin
from .models import (
    Category,
    FormationType,
    Formation,
    Curriculum,
    FormationReview,
    OnlineFormation,
    OnlineFormationModule,
    Lesson,
    OnlineFormationEnrollment,
    LessonProgress,
    Quiz,
    QuizQuestion,
    QuizAnswer,
    QuizAttempt,
    QuizResponse,
    Certificate,
    CertificateVerification,
    LiveStream,
    LiveStreamAttendance,
    LiveStreamMessage,
    UserInteraction,
    ContentRecommendation,
    UserPreference,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    list_filter = ["is_active"]


@admin.register(FormationType)
class FormationTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class CurriculumInline(admin.TabularInline):
    model = Curriculum
    extra = 1


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "coach",
        "category",
        "delivery_mode",
        "price",
        "status",
        "start_date",
    ]
    list_filter = ["status", "delivery_mode", "level", "category"]
    search_fields = ["title", "coach__username"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CurriculumInline]
    date_hierarchy = "start_date"


@admin.register(FormationReview)
class FormationReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "formation", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["user__username", "formation__title"]


# Online Formations
class OnlineFormationModuleInline(admin.TabularInline):
    model = OnlineFormationModule
    extra = 1
    ordering = ["order"]


@admin.register(OnlineFormation)
class OnlineFormationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "coach",
        "category",
        "access_type",
        "credit_cost",
        "total_enrolled",
        "is_published",
    ]
    list_filter = ["access_type", "is_published", "is_featured", "level", "category"]
    search_fields = ["title", "coach__username"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [OnlineFormationModuleInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ["order"]


@admin.register(OnlineFormationModule)
class OnlineFormationModuleAdmin(admin.ModelAdmin):
    list_display = ["online_formation", "title", "order", "requires_previous_module"]
    list_filter = ["requires_previous_module"]
    search_fields = ["title", "online_formation__title"]
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        "module",
        "title",
        "order",
        "lesson_type",
        "is_preview",
        "is_downloadable",
    ]
    list_filter = ["lesson_type", "is_preview", "is_downloadable"]
    search_fields = ["title", "module__title"]


@admin.register(OnlineFormationEnrollment)
class OnlineFormationEnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "online_formation",
        "progress_percentage",
        "completed",
        "payment_date",
    ]
    list_filter = ["completed", "certificate_issued"]
    search_fields = ["user__username", "online_formation__title"]
    date_hierarchy = "payment_date"


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = [
        "enrollment",
        "lesson",
        "started",
        "completed",
        "marked_as_studied",
        "completion_percentage",
    ]
    list_filter = ["started", "completed", "marked_as_studied"]
    search_fields = ["enrollment__user__username", "lesson__title"]


# Quiz System
class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    ordering = ["order"]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "creator",
        "visibility",
        "passing_score",
        "is_published",
        "total_attempts",
        "average_score",
    ]
    list_filter = [
        "visibility",
        "is_published",
        "randomize_questions",
        "randomize_answers",
    ]
    search_fields = ["title", "creator__username"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [QuizQuestionInline]


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 4
    ordering = ["order"]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ["quiz", "order", "question_type", "points"]
    list_filter = ["question_type"]
    search_fields = ["quiz__title", "question_text"]
    inlines = [QuizAnswerInline]


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "answer_text", "is_correct", "order"]
    list_filter = ["is_correct"]
    search_fields = ["question__quiz__title", "answer_text"]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "quiz",
        "attempt_number",
        "percentage",
        "passed",
        "started_at",
        "completed_at",
    ]
    list_filter = ["passed"]
    search_fields = ["user__username", "quiz__title"]
    date_hierarchy = "started_at"


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ["attempt", "question", "is_correct", "points_earned"]
    list_filter = ["is_correct"]
    search_fields = ["attempt__user__username", "question__question_text"]


# Certificate System
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "certificate_type",
        "verification_code",
        "is_public",
        "issued_at",
    ]
    list_filter = ["certificate_type", "is_public", "is_verified"]
    search_fields = ["title", "user__username", "verification_code"]
    readonly_fields = ["verification_code", "issued_at"]
    date_hierarchy = "issued_at"


@admin.register(CertificateVerification)
class CertificateVerificationAdmin(admin.ModelAdmin):
    list_display = [
        "certificate",
        "verified_by_ip",
        "verifier_organization",
        "verified_at",
    ]
    list_filter = ["verified_at"]
    search_fields = [
        "certificate__verification_code",
        "verifier_email",
        "verifier_organization",
    ]
    date_hierarchy = "verified_at"


# Live Streaming System
@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "host",
        "status",
        "scheduled_start",
        "current_viewers",
        "peak_viewers",
    ]
    list_filter = ["status", "is_public", "requires_enrollment", "chat_enabled"]
    search_fields = ["title", "host__username"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "scheduled_start"
    filter_horizontal = ["co_hosts"]


@admin.register(LiveStreamAttendance)
class LiveStreamAttendanceAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "stream",
        "joined_at",
        "watch_duration_minutes",
        "eligible_for_certificate",
    ]
    list_filter = ["eligible_for_certificate"]
    search_fields = ["user__username", "stream__title"]
    date_hierarchy = "joined_at"


@admin.register(LiveStreamMessage)
class LiveStreamMessageAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "stream",
        "message_type",
        "is_pinned",
        "is_answered",
        "created_at",
    ]
    list_filter = ["message_type", "is_pinned", "is_answered"]
    search_fields = ["user__username", "stream__title", "content"]
    date_hierarchy = "created_at"


# AI Recommendation System
@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "interaction_type",
        "formation",
        "online_formation",
        "created_at",
    ]
    list_filter = ["interaction_type", "device_type", "created_at"]
    search_fields = ["user__username", "search_query"]
    date_hierarchy = "created_at"


@admin.register(ContentRecommendation)
class ContentRecommendationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "reason",
        "confidence_score",
        "shown",
        "clicked",
        "enrolled",
        "created_at",
    ]
    list_filter = ["reason", "shown", "clicked", "enrolled", "model_version"]
    search_fields = ["user__username"]
    date_hierarchy = "created_at"


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "preferred_level",
        "preferred_delivery",
        "preferred_language",
        "recommendation_frequency",
    ]
    list_filter = [
        "preferred_level",
        "preferred_delivery",
        "preferred_language",
        "recommendation_frequency",
    ]
    search_fields = ["user__username"]
    filter_horizontal = ["favorite_categories"]
