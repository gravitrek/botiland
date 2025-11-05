from django.contrib import admin
from .models import Booking, BookingNotification, Attendance


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_code', 'user', 'formation', 'status', 'amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['booking_code', 'user__username', 'formation__title']
    readonly_fields = ['booking_code']


@admin.register(BookingNotification)
class BookingNotificationAdmin(admin.ModelAdmin):
    list_display = ['booking', 'notification_type', 'sent_at']
    list_filter = ['notification_type', 'sent_at']
    search_fields = ['booking__booking_code']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['booking', 'attended', 'check_in_time', 'check_out_time']
    list_filter = ['attended']
    search_fields = ['booking__booking_code', 'booking__user__username']
