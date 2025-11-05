"""
Multi-Tenant Middleware for JoliTableau
Handles custom domains and subdomains for artists/galleries
"""

from core.models import CustomDomain


class MultiTenantMiddleware:
    """
    Middleware to detect custom domains and attach the appropriate user context
    Allows artists/galleries to have their own subdomain or custom domain

    Examples:
    - picasso.jolitableau.com → Subdomain
    - artiste.com → Custom domain (CNAME to JoliTableau)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]  # Remove port if present

        # Check if this is a custom domain
        try:
            custom_domain = CustomDomain.objects.select_related('user').get(
                domain=host,
                status=CustomDomain.DomainStatus.ACTIVE
            )
            request.custom_domain = custom_domain
            request.domain_owner = custom_domain.user
        except CustomDomain.DoesNotExist:
            request.custom_domain = None
            request.domain_owner = None

        response = self.get_response(request)
        return response
