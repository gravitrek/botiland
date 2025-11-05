"""
URL configuration for MegaGoals project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# Non-i18n URLs
urlpatterns = [
    path('accounts/', include('allauth.urls')),
]

# i18n-enabled URLs
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # App URLs
    path('goals/', include('goals.urls')),
    path('community/', include('community.urls')),
    path('coaching/', include('coaching.urls')),
    path('gamification/', include('gamification.urls')),
    path('ai-coach/', include('ai_coach.urls')),
    path('payments/', include('payments.urls')),
    path('analytics/', include('analytics.urls')),
    path('users/', include('users.urls')),
)

# Static and media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
