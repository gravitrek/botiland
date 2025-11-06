from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import LandingPage
from .serializers import LandingPageSerializer, LandingPageCreateSerializer, LandingPagePublicSerializer


class LandingPageViewSet(viewsets.ModelViewSet):
    """Landing Page CRUD operations"""
    serializer_class = LandingPageSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active', 'is_published']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'views', 'conversions']

    def get_queryset(self):
        return LandingPage.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return LandingPageCreateSerializer
        return LandingPageSerializer

    def perform_create(self, serializer):
        landing_page = serializer.save()
        # Update user's landing page count
        self.request.user.landing_pages_created += 1
        self.request.user.save()

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def public(self, request, pk=None):
        """Get public landing page"""
        landing_page = get_object_or_404(LandingPage, id=pk, is_active=True, is_published=True)
        # Increment view count
        landing_page.views += 1
        landing_page.save(update_fields=['views'])
        serializer = LandingPagePublicSerializer(landing_page)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a landing page"""
        page = self.get_object()
        page.pk = None
        page.id = None
        page.slug = f"{page.slug}-copy"
        page.name = f"{page.name} (Copy)"
        page.is_published = False
        page.views = 0
        page.conversions = 0
        page.save()

        # Update user's landing page count
        request.user.landing_pages_created += 1
        request.user.save()

        serializer = self.get_serializer(page)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def toggle_publish(self, request, pk=None):
        """Toggle landing page published status"""
        page = self.get_object()
        page.is_published = not page.is_published
        page.save(update_fields=['is_published'])
        return Response({'is_published': page.is_published})
