from rest_framework import serializers
from .models import LandingPage


class LandingPageSerializer(serializers.ModelSerializer):
    """Landing page serializer"""

    user_email = serializers.EmailField(source='user.email', read_only=True)
    form_name = serializers.CharField(source='form.name', read_only=True)

    class Meta:
        model = LandingPage
        fields = [
            'id', 'user', 'user_email', 'name', 'description', 'slug',
            'content', 'form', 'form_name',
            'meta_title', 'meta_description', 'meta_keywords',
            'theme', 'custom_css', 'custom_js',
            'is_active', 'is_published',
            'views', 'conversions', 'conversion_rate',
            'tracking_code',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'user_email', 'views', 'conversions', 'created_at', 'updated_at']

    def validate_slug(self, value):
        user = self.context['request'].user
        if self.instance:
            if LandingPage.objects.filter(user=user, slug=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A landing page with this slug already exists.")
        else:
            if LandingPage.objects.filter(user=user, slug=value).exists():
                raise serializers.ValidationError("A landing page with this slug already exists.")
        return value


class LandingPageCreateSerializer(serializers.ModelSerializer):
    """Landing page creation serializer"""

    class Meta:
        model = LandingPage
        fields = [
            'name', 'description', 'slug', 'content', 'form',
            'meta_title', 'meta_description', 'meta_keywords',
            'theme', 'custom_css', 'custom_js',
            'is_active', 'is_published', 'tracking_code'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return LandingPage.objects.create(user=user, **validated_data)


class LandingPagePublicSerializer(serializers.ModelSerializer):
    """Public landing page serializer"""

    class Meta:
        model = LandingPage
        fields = [
            'id', 'name', 'content', 'meta_title', 'meta_description',
            'meta_keywords', 'theme', 'custom_css', 'custom_js', 'tracking_code'
        ]
