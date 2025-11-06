from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer for profile"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'company_name', 'phone_number', 'website',
            'subscription_plan', 'subscription_active',
            'subscription_start_date', 'subscription_end_date',
            'forms_created', 'landing_pages_created',
            'leads_this_month', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'subscription_plan', 'subscription_active',
            'subscription_start_date', 'subscription_end_date',
            'forms_created', 'landing_pages_created',
            'leads_this_month', 'is_verified',
            'created_at', 'updated_at'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'company_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
