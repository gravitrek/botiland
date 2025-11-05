"""
Context processors for MegaGoals platform.
"""

from django.conf import settings


def site_settings(request):
    """Add site-wide settings to template context."""
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'DEBUG': settings.DEBUG,
    }

    # Add user-specific data if authenticated
    if request.user.is_authenticated:
        context['user_credits'] = request.user.credits
        context['user_level'] = request.user.level
        context['user_xp'] = request.user.xp
        context['user_streak'] = request.user.current_streak
        context['unread_notifications'] = request.user.notifications.filter(read=False).count()

    return context
