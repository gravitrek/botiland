"""
URL patterns for payments app.
"""
from django.urls import path
from .views import (
    create_checkout,
    confirm_payment,
    payment_history,
    cancel_subscription,
)

app_name = 'payments'

urlpatterns = [
    path('create-checkout/', create_checkout, name='create_checkout'),
    path('confirm/', confirm_payment, name='confirm_payment'),
    path('history/', payment_history, name='payment_history'),
    path('cancel-subscription/', cancel_subscription, name='cancel_subscription'),
]
