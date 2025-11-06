"""
URL patterns for analytics app.
"""
from django.urls import path
from .views import QRCodeAnalyticsView, UserDashboardView

app_name = 'analytics'

urlpatterns = [
    path('<uuid:qr_id>/', QRCodeAnalyticsView.as_view(), name='qr_analytics'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
]
