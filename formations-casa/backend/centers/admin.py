from django.contrib import admin
from .models import TrainingCenter, Room, RoomImage, RoomAvailability, CenterReview


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    fields = ["name", "capacity", "hourly_rate", "is_active"]


@admin.register(TrainingCenter)
class TrainingCenterAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "city", "is_approved", "average_rating"]
    list_filter = ["is_approved", "city"]
    search_fields = ["name", "owner__username"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "training_center", "capacity", "hourly_rate", "is_active"]
    list_filter = ["is_active", "layout_type"]
    search_fields = ["name", "training_center__name"]


@admin.register(RoomAvailability)
class RoomAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["room", "date", "start_time", "end_time", "is_available"]
    list_filter = ["is_available", "date"]
    search_fields = ["room__name"]


@admin.register(CenterReview)
class CenterReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "center", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["user__username", "center__name"]
