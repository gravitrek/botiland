"""
Views for industry-specific features.
"""
from rest_framework import generics, permissions
from .models import RestaurantMenu, VCard, WiFiCredentials, EventInfo


class IndustryFeatureView(generics.RetrieveUpdateAPIView):
    """Base view for industry features."""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(qr_code__user=self.request.user)
