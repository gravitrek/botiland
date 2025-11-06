"""
URL patterns for QR code redirects (short URLs).
"""
from django.urls import path
from .views import redirect_short_url

urlpatterns = [
    path('<str:short_code>/', redirect_short_url, name='redirect'),
]
