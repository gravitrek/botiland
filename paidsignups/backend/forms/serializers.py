from rest_framework import serializers
from .models import Form


class FormSerializer(serializers.ModelSerializer):
    """Form serializer"""

    user_email = serializers.EmailField(source='user.email', read_only=True)
    conversion_rate = serializers.SerializerMethodField()

    class Meta:
        model = Form
        fields = [
            'id', 'user', 'user_email', 'name', 'description', 'slug',
            'fields', 'submit_button_text', 'success_message', 'redirect_url',
            'send_notification', 'notification_email', 'notification_subject',
            'theme', 'is_active', 'is_published',
            'views', 'submissions', 'conversion_rate',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'user_email', 'views', 'submissions', 'created_at', 'updated_at']

    def get_conversion_rate(self, obj):
        if obj.views == 0:
            return 0
        return round((obj.submissions / obj.views) * 100, 2)

    def validate_slug(self, value):
        user = self.context['request'].user
        if self.instance:
            # Updating existing form
            if Form.objects.filter(user=user, slug=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A form with this slug already exists.")
        else:
            # Creating new form
            if Form.objects.filter(user=user, slug=value).exists():
                raise serializers.ValidationError("A form with this slug already exists.")
        return value


class FormCreateSerializer(serializers.ModelSerializer):
    """Form creation serializer"""

    class Meta:
        model = Form
        fields = [
            'name', 'description', 'slug', 'fields',
            'submit_button_text', 'success_message', 'redirect_url',
            'send_notification', 'notification_email', 'notification_subject',
            'theme', 'is_active', 'is_published'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return Form.objects.create(user=user, **validated_data)


class FormPublicSerializer(serializers.ModelSerializer):
    """Public form serializer (for embedding)"""

    class Meta:
        model = Form
        fields = [
            'id', 'name', 'fields', 'submit_button_text',
            'success_message', 'redirect_url', 'theme'
        ]
