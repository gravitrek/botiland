"""
Quick script to set up admin interfaces for all models.
Run this after all models are created.
"""

# This file documents the admin setup that should be added to each app's admin.py

ADMIN_CONFIGS = {
    'restaurants/admin.py': '''from django.contrib import admin
from .models import Restaurant, RestaurantSettings

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'restaurant_type', 'subscription_plan', 'subscription_status', 'is_active', 'created_at')
    list_filter = ('restaurant_type', 'subscription_plan', 'subscription_status', 'is_active', 'is_verified')
    search_fields = ('name', 'email', 'phone', 'city')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(RestaurantSettings)
class RestaurantSettingsAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'currency', 'timezone', 'email_notifications', 'whatsapp_notifications')
    list_filter = ('email_notifications', 'whatsapp_notifications', 'auto_accept_orders')
''',

    'menus/admin.py': '''from django.contrib import admin
from .models import MenuCategory, MenuItem, MenuItemModifier, MenuItemModifierOption, MenuItemModifierLink, MenuItemVariant

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'display_order', 'is_active', 'created_at')
    list_filter = ('is_active', 'restaurant')
    search_fields = ('name', 'description')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'restaurant', 'price', 'is_available', 'is_featured', 'stock_quantity')
    list_filter = ('is_available', 'is_featured', 'is_popular', 'dietary_type', 'category__restaurant')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(MenuItemModifier)
class MenuItemModifierAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'modifier_type', 'is_required', 'is_active')
    list_filter = ('modifier_type', 'is_required', 'is_active')

@admin.register(MenuItemModifierOption)
class MenuItemModifierOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'modifier', 'price_adjustment', 'is_default', 'is_available')
    list_filter = ('is_default', 'is_available')

@admin.register(MenuItemModifierLink)
class MenuItemModifierLinkAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'modifier', 'is_required', 'display_order')

@admin.register(MenuItemVariant)
class MenuItemVariantAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'name', 'price', 'is_available', 'is_default')
''',

    'orders/admin.py': '''from django.contrib import admin
from .models import Order, OrderItem, OrderItemModifier, OrderStatusHistory

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'restaurant', 'customer_name', 'order_type', 'order_status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('order_type', 'order_status', 'payment_status', 'restaurant', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('id', 'order_number', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item_name', 'quantity', 'unit_price', 'total_price', 'is_prepared')
    list_filter = ('is_prepared', 'order__restaurant')
    search_fields = ('item_name', 'order__order_number')

@admin.register(OrderItemModifier)
class OrderItemModifierAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'modifier_name', 'option_name', 'price_adjustment')

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'old_status', 'new_status', 'changed_by', 'timestamp')
    list_filter = ('new_status', 'timestamp')
    readonly_fields = ('timestamp',)
''',

    'tables/admin.py': '''from django.contrib import admin
from .models import Table, TableReservation, TableSession

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'restaurant', 'capacity', 'status', 'section', 'is_active')
    list_filter = ('status', 'is_active', 'restaurant', 'section')
    search_fields = ('table_number', 'table_name')
    readonly_fields = ('id', 'qr_code', 'qr_code_url', 'created_at', 'updated_at')

@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'restaurant', 'reservation_date', 'reservation_time', 'party_size', 'status')
    list_filter = ('status', 'reservation_date', 'restaurant')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    date_hierarchy = 'reservation_date'

@admin.register(TableSession)
class TableSessionAdmin(admin.ModelAdmin):
    list_display = ('table', 'restaurant', 'party_size', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'restaurant', 'start_time')
''',

    'customers/admin.py': '''from django.contrib import admin
from .models import Customer, CustomerAddress

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'loyalty_points', 'total_orders', 'total_spent', 'last_order_date')
    list_filter = ('restaurant', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_type', 'city', 'is_default')
    list_filter = ('address_type', 'is_default')
''',

    'payments/admin.py': '''from django.contrib import admin
from .models import Payment, SubscriptionPayment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'restaurant', 'payment_method', 'payment_status', 'amount', 'currency', 'created_at')
    list_filter = ('payment_method', 'payment_status', 'restaurant', 'created_at')
    search_fields = ('order__order_number', 'transaction_id', 'stripe_payment_intent_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'subscription_plan', 'amount', 'payment_status', 'billing_period_start', 'billing_period_end')
    list_filter = ('payment_status', 'subscription_plan', 'created_at')
    readonly_fields = ('id', 'created_at')
''',

    'notifications/admin.py': '''from django.contrib import admin
from .models import Notification, EmailTemplate

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'channel', 'status', 'title', 'sent_at', 'created_at')
    list_filter = ('notification_type', 'channel', 'status', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'restaurant', 'is_active', 'created_at')
    list_filter = ('template_type', 'is_active')
    search_fields = ('name', 'subject')
''',

    'analytics/admin.py': '''from django.contrib import admin
from .models import DailySalesReport, MenuItemAnalytics, CustomerBehavior

@admin.register(DailySalesReport)
class DailySalesReportAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'date', 'total_orders', 'total_revenue', 'average_order_value', 'unique_customers')
    list_filter = ('date', 'restaurant')
    date_hierarchy = 'date'
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(MenuItemAnalytics)
class MenuItemAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'date', 'times_ordered', 'quantity_sold', 'total_revenue', 'profit')
    list_filter = ('date', 'restaurant')
    search_fields = ('menu_item__name',)
    date_hierarchy = 'date'

@admin.register(CustomerBehavior)
class CustomerBehaviorAdmin(admin.ModelAdmin):
    list_display = ('customer', 'restaurant', 'average_order_value', 'order_frequency', 'lifetime_value', 'is_at_risk')
    list_filter = ('is_at_risk', 'restaurant')
'''
}

print("Admin configurations ready. Apply them to respective admin.py files.")
