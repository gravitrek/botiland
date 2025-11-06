"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import viewsets
from accounts.views import UserViewSet, UserRegistrationView, UserProfileView, ChangePasswordView
from forms.views import FormViewSet
from landing_pages.views import LandingPageViewSet
from leads.views import LeadViewSet, LeadSubmissionView
from subscriptions.views import SubscriptionViewSet, PaymentViewSet, PayPalWebhookView

# Create router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'forms', FormViewSet, basename='form')
router.register(r'landing-pages', LandingPageViewSet, basename='landing-page')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Authentication
    path('api/auth/register/', UserRegistrationView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', UserProfileView.as_view(), name='profile'),
    path('api/auth/change-password/', ChangePasswordView.as_view(), name='change_password'),

    # API endpoints
    path('api/', include(router.urls)),

    # Public endpoints
    path('api/submit/', LeadSubmissionView.as_view(), name='lead_submission'),
    path('api/paypal/webhook/', PayPalWebhookView.as_view(), name='paypal_webhook'),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
