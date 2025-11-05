from django.contrib import admin
from .models import Feature, FeatureUsage, CreditPurchase, Subscription


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ["name", "feature_type", "credits_cost", "is_active"]
    list_filter = ["feature_type", "is_active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(FeatureUsage)
class FeatureUsageAdmin(admin.ModelAdmin):
    list_display = ["user", "feature", "credits_spent", "created_at"]
    list_filter = ["feature", "created_at"]
    search_fields = ["user__username", "feature__name"]


@admin.register(CreditPurchase)
class CreditPurchaseAdmin(admin.ModelAdmin):
    list_display = ["user", "credits", "amount", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "transaction_id"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "plan_type",
        "status",
        "start_date",
        "end_date",
        "monthly_credits",
    ]
    list_filter = ["plan_type", "status"]
    search_fields = ["user__username"]
