"""
Views for analytics.
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import QRScan, QRAnalytics
from qrcodes.models import QRCode


class QRCodeAnalyticsView(APIView):
    """Get analytics for a specific QR code."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, qr_id):
        qr_code = QRCode.objects.filter(id=qr_id, user=request.user).first()
        if not qr_code:
            return Response({'error': 'QR code not found'}, status=404)

        # Get scan statistics
        scans = QRScan.objects.filter(qr_code=qr_code)

        # Top countries
        top_countries = scans.values('country').annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        # Top devices
        top_devices = scans.values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        # Top browsers
        top_browsers = scans.values('browser').annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        return Response({
            'total_scans': qr_code.total_scans,
            'unique_scans': qr_code.unique_scans,
            'last_scanned_at': qr_code.last_scanned_at,
            'top_countries': list(top_countries),
            'top_devices': list(top_devices),
            'top_browsers': list(top_browsers),
        })


class UserDashboardView(APIView):
    """Get dashboard statistics for user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        qr_codes = QRCode.objects.filter(user=user)

        total_qr_codes = qr_codes.count()
        active_qr_codes = qr_codes.filter(is_active=True).count()
        total_scans = sum(qr.total_scans for qr in qr_codes)

        return Response({
            'total_qr_codes': total_qr_codes,
            'active_qr_codes': active_qr_codes,
            'total_scans': total_scans,
            'qr_code_limit': user.qr_code_limit,
            'scan_limit': user.scan_limit,
        })
