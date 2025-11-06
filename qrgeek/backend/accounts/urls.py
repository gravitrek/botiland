"""
URL patterns for accounts app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    PasswordChangeView,
    SubscriptionPlanListView,
    UserSubscriptionView,
    SubscriptionUpgradeView,
    DeleteAccountView,
)

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('account/', DeleteAccountView.as_view(), name='delete_account'),

    # Subscription
    path('plans/', SubscriptionPlanListView.as_view(), name='plans'),
    path('subscription/', UserSubscriptionView.as_view(), name='subscription'),
    path('subscription/upgrade/', SubscriptionUpgradeView.as_view(), name='subscription_upgrade'),
]
