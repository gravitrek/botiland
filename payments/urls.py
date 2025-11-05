"""
URLs for Payments app.
"""

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('credits/', views.buy_credits, name='buy_credits'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('transactions/', views.transactions, name='transactions'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
