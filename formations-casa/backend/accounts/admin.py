from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CoachProfile, TrainingCenterProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_approved', 'credits', 'total_points', 'level']
    list_filter = ['role', 'is_approved', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extended Profile', {
            'fields': ('phone', 'avatar', 'bio', 'role', 'address', 'city')
        }),
        ('Approval', {
            'fields': ('is_approved', 'approved_at', 'approved_by')
        }),
        ('Gamification', {
            'fields': ('credits', 'total_points', 'level')
        }),
    )


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'years_experience', 'total_formations', 'total_students', 'average_rating']
    search_fields = ['user__username', 'user__email', 'specializations']
    list_filter = ['years_experience']


@admin.register(TrainingCenterProfile)
class TrainingCenterProfileAdmin(admin.ModelAdmin):
    list_display = ['center_name', 'user', 'total_rooms', 'average_rating']
    search_fields = ['center_name', 'user__username']
    list_filter = ['has_parking', 'has_wifi', 'has_cafe']
