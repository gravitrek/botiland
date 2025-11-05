from django.contrib import admin
from .models import Payment, PaymentInstruction, Reconciliation


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['booking__booking_code', 'transaction_reference']


@admin.register(PaymentInstruction)
class PaymentInstructionAdmin(admin.ModelAdmin):
    list_display = ['coach', 'formation', 'bank_name', 'is_default']
    list_filter = ['is_default', 'bank_name']
    search_fields = ['coach__username', 'formation__title']


@admin.register(Reconciliation)
class ReconciliationAdmin(admin.ModelAdmin):
    list_display = ['coach', 'formation', 'total_expected', 'total_received', 'is_completed']
    list_filter = ['is_completed', 'period_start']
    search_fields = ['coach__username', 'formation__title']
