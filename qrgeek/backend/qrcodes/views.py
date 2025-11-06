"""
Views for QR code management.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import QRCode, Tag, QRTemplate
from .serializers import (
    QRCodeListSerializer, QRCodeDetailSerializer,
    QRCodeCreateSerializer, TagSerializer,
    QRTemplateSerializer, BulkQRCreateSerializer
)
from .utils import generate_qr_code, get_qr_content
from analytics.models import QRScan
import user_agents


class QRCodeListCreateView(generics.ListCreateAPIView):
    """List and create QR codes."""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QRCodeCreateSerializer
        return QRCodeListSerializer

    def get_queryset(self):
        return QRCode.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        qr_code = serializer.save()
        # Generate QR code image
        self.generate_qr_image(qr_code)


    def generate_qr_image(self, qr_code):
        """Generate and save QR code image."""
        content = get_qr_content(qr_code)

        # Use short URL if tracking is enabled
        if qr_code.enable_tracking:
            content = qr_code.short_url

        # Generate QR image
        qr_image = generate_qr_code(
            content,
            size=qr_code.size,
            foreground_color=qr_code.foreground_color,
            background_color=qr_code.background_color,
            error_correction=qr_code.error_correction,
            logo=qr_code.logo.file if qr_code.logo else None,
        )

        # Save image
        qr_code.qr_image.save(
            f'qr_{qr_code.short_code}.png',
            qr_image,
            save=True
        )


class QRCodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a QR code."""
    serializer_class = QRCodeDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QRCode.objects.filter(user=self.request.user)


class QRCodeDownloadView(generics.RetrieveAPIView):
    """Download QR code image."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        qr_code = get_object_or_404(QRCode, pk=pk, user=request.user)

        if not qr_code.qr_image:
            return Response(
                {'error': 'QR code image not generated yet'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Return file
        response = HttpResponse(qr_code.qr_image.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{qr_code.name}.png"'
        return response


class BulkQRCodeCreateView(generics.CreateAPIView):
    """Bulk create QR codes."""
    serializer_class = BulkQRCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagListCreateView(generics.ListCreateAPIView):
    """List and create tags."""
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QRTemplateListView(generics.ListAPIView):
    """List QR code templates."""
    queryset = QRTemplate.objects.filter(is_active=True)
    serializer_class = QRTemplateSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
def redirect_short_url(request, short_code):
    """Redirect short URL and track scan."""
    qr_code = get_object_or_404(QRCode, short_code=short_code)

    # Check if expired
    if qr_code.is_expired or not qr_code.is_active:
        return Response(
            {'error': 'QR code is no longer active'},
            status=status.HTTP_410_GONE
        )

    # Track scan if enabled
    if qr_code.enable_tracking:
        track_qr_scan(request, qr_code)

    # Get destination URL
    destination = qr_code.content.get('url', '/')

    return redirect(destination)


def track_qr_scan(request, qr_code):
    """Track QR code scan."""
    from analytics.utils import get_client_ip, parse_user_agent, get_location

    ip_address = get_client_ip(request)
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = user_agents.parse(user_agent_string)

    # Create scan record
    QRScan.objects.create(
        qr_code=qr_code,
        ip_address=ip_address,
        device_type=user_agent.device.family,
        os=user_agent.os.family,
        browser=user_agent.browser.family,
        user_agent=user_agent_string,
        referer=request.META.get('HTTP_REFERER', ''),
    )

    # Increment counters
    qr_code.increment_scan()
