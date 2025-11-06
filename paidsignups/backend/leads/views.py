from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Lead
from forms.models import Form
from .serializers import LeadSerializer, LeadCreateSerializer, LeadStatsSerializer


class LeadViewSet(viewsets.ModelViewSet):
    """Lead CRUD operations"""
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['form', 'status', 'source_landing_page']
    search_fields = ['data']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        return Lead.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get lead statistics"""
        leads = self.get_queryset()
        now = timezone.now()

        stats = {
            'total_leads': leads.count(),
            'new_leads': leads.filter(status='NEW').count(),
            'contacted_leads': leads.filter(status='CONTACTED').count(),
            'qualified_leads': leads.filter(status='QUALIFIED').count(),
            'converted_leads': leads.filter(status='CONVERTED').count(),
            'lost_leads': leads.filter(status='LOST').count(),
            'leads_this_month': leads.filter(created_at__gte=now - timedelta(days=30)).count(),
            'leads_this_week': leads.filter(created_at__gte=now - timedelta(days=7)).count(),
            'leads_today': leads.filter(created_at__gte=now - timedelta(days=1)).count(),
        }

        serializer = LeadStatsSerializer(stats)
        return Response(serializer.data)


class LeadSubmissionView(generics.CreateAPIView):
    """Public form submission endpoint"""
    serializer_class = LeadCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lead = serializer.save()
        form = lead.form

        # Increment form submissions
        form.submissions += 1
        form.save(update_fields=['submissions'])

        # Update user's lead count
        form.user.leads_this_month += 1
        form.user.save(update_fields=['leads_this_month'])

        # Send email notification if enabled
        if form.send_notification and form.notification_email:
            try:
                send_mail(
                    subject=form.notification_subject,
                    message=f"New lead submission for {form.name}\n\nData: {lead.data}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[form.notification_email],
                    fail_silently=True,
                )
                lead.email_sent = True
                lead.email_sent_at = timezone.now()
                lead.save(update_fields=['email_sent', 'email_sent_at'])
            except Exception as e:
                pass

        return Response({
            'success': True,
            'message': form.success_message,
            'redirect_url': form.redirect_url,
        }, status=status.HTTP_201_CREATED)
