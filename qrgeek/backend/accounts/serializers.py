"""
Serializers for user authentication and management.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, SubscriptionPlan, UserSubscription


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'full_name', 'company_name', 'industry'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.'
                )

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".'
            )


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    qr_code_count = serializers.SerializerMethodField()
    subscription_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'full_name', 'company_name',
            'industry', 'is_verified', 'qr_code_count',
            'subscription_name', 'qr_code_limit', 'scan_limit',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'email', 'is_verified', 'created_at', 'updated_at'
        ]

    def get_qr_code_count(self, obj):
        from qrcodes.models import QRCode
        return QRCode.objects.filter(user=obj, is_active=True).count()

    def get_subscription_name(self, obj):
        if obj.subscription_plan:
            return obj.subscription_plan.name
        return 'Free'


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for subscription plans."""
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'billing_period', 'qr_limit', 'scan_limit',
            'features', 'is_featured'
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for user subscriptions."""
    plan_details = SubscriptionPlanSerializer(source='plan', read_only=True)

    class Meta:
        model = UserSubscription
        fields = [
            'id', 'plan', 'plan_details', 'status', 'starts_at',
            'ends_at', 'auto_renew', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for changing password."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
