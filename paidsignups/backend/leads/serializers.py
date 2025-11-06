from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    """Lead serializer"""

    form_name = serializers.CharField(source='form.name', read_only=True)
    landing_page_name = serializers.CharField(source='source_landing_page.name', read_only=True, allow_null=True)

    class Meta:
        model = Lead
        fields = [
            'id', 'form', 'form_name', 'user', 'data',
            'source_url', 'source_landing_page', 'landing_page_name',
            'referrer', 'user_agent', 'ip_address',
            'status', 'notes',
            'email_sent', 'email_sent_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'email_sent', 'email_sent_at', 'created_at', 'updated_at']


class LeadCreateSerializer(serializers.ModelSerializer):
    """Lead creation serializer (for public form submissions)"""

    class Meta:
        model = Lead
        fields = [
            'form', 'data', 'source_url', 'source_landing_page',
            'referrer', 'user_agent', 'ip_address'
        ]

    def create(self, validated_data):
        # Get the form to determine the user
        form = validated_data.get('form')
        return Lead.objects.create(user=form.user, **validated_data)


class LeadStatsSerializer(serializers.Serializer):
    """Lead statistics serializer"""

    total_leads = serializers.IntegerField()
    new_leads = serializers.IntegerField()
    contacted_leads = serializers.IntegerField()
    qualified_leads = serializers.IntegerField()
    converted_leads = serializers.IntegerField()
    lost_leads = serializers.IntegerField()
    leads_this_month = serializers.IntegerField()
    leads_this_week = serializers.IntegerField()
    leads_today = serializers.IntegerField()
