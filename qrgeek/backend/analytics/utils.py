"""
Utility functions for analytics.
"""


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_user_agent(user_agent_string):
    """Parse user agent string."""
    import user_agents
    return user_agents.parse(user_agent_string)


def get_location(ip_address):
    """Get location from IP address (placeholder)."""
    # TODO: Implement with GeoIP2 or similar service
    return {
        'country': '',
        'city': '',
        'latitude': None,
        'longitude': None,
    }
