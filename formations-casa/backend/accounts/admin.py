from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    CoachProfile,
    TrainingCenterProfile,
    VerificationRequest,
    PlatformSettings,
    CreditTransaction,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "username",
        "email",
        "role",
        "is_verified",
        "is_approved",
        "credits",
        "total_points",
        "level",
    ]
    list_filter = ["role", "is_verified", "is_approved", "is_staff", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Extended Profile",
            {"fields": ("phone", "avatar", "bio", "role", "address", "city")},
        ),
        (
            "Verification",
            {
                "fields": (
                    "is_verified",
                    "verification_requested",
                    "verification_requested_at",
                    "verified_at",
                    "verified_by",
                )
            },
        ),
        (
            "Approval (Legacy)",
            {
                "fields": ("is_approved", "approved_at", "approved_by"),
                "classes": ("collapse",),
            },
        ),
        ("Gamification", {"fields": ("credits", "total_points", "level")}),
    )


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "years_experience",
        "total_formations",
        "total_students",
        "average_rating",
    ]
    search_fields = ["user__username", "user__email", "specializations"]
    list_filter = ["years_experience"]


@admin.register(TrainingCenterProfile)
class TrainingCenterProfileAdmin(admin.ModelAdmin):
    list_display = ["center_name", "user", "total_rooms", "average_rating"]
    search_fields = ["center_name", "user__username"]
    list_filter = ["has_parking", "has_wifi", "has_cafe"]


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "status",
        "credits_paid",
        "created_at",
        "reviewed_at",
        "reviewed_by",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "user__email"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        ("User Information", {"fields": ("user", "credits_paid", "created_at")}),
        (
            "Request Details",
            {"fields": ("motivation", "credentials", "website", "social_proof")},
        ),
        ("Documents", {"fields": ("id_document", "credential_document")}),
        ("Review", {"fields": ("status", "admin_notes", "reviewed_by", "reviewed_at")}),
    )


@admin.register(PlatformSettings)
class PlatformSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "credit_price_mad",
        "verification_badge_cost",
        "default_platform_percentage",
        "updated_at",
    ]

    fieldsets = (
        ("Credit Pricing", {"fields": ("credit_price_mad",)}),
        (
            "Feature Costs",
            {
                "fields": (
                    "verification_badge_cost",
                    "featured_formation_cost",
                    "premium_listing_cost",
                )
            },
        ),
        ("Revenue Sharing", {"fields": ("default_platform_percentage",)}),
        (
            "Credit Packages",
            {
                "fields": (
                    ("credit_package_small", "credit_package_small_bonus"),
                    ("credit_package_medium", "credit_package_medium_bonus"),
                    ("credit_package_large", "credit_package_large_bonus"),
                    ("credit_package_xl", "credit_package_xl_bonus"),
                )
            },
        ),
        ("Other Settings", {"fields": ("min_withdrawal_credits",)}),
    )

    def has_add_permission(self, request):
        # Only allow one settings instance
        return not PlatformSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting settings
        return False


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "transaction_type",
        "amount",
        "balance_after",
        "payment_status",
        "created_at",
    ]
    list_filter = ["transaction_type", "payment_status", "created_at"]
    search_fields = ["user__username", "description"]
    readonly_fields = ["created_at", "balance_after"]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Transaction Info",
            {
                "fields": (
                    "user",
                    "transaction_type",
                    "amount",
                    "balance_after",
                    "description",
                )
            },
        ),
        ("Related Objects", {"fields": ("online_formation", "verification_request")}),
        (
            "Payment Details",
            {"fields": ("payment_amount_mad", "payment_proof", "payment_status")},
        ),
        ("Admin", {"fields": ("processed_by", "created_at")}),
    )
