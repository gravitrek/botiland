from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CoachProfile, TrainingCenterProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'avatar', 'bio', 'role', 'is_approved',
            'credits', 'total_points', 'level', 'address', 'city',
            'created_at'
        ]
        read_only_fields = ['id', 'is_approved', 'credits', 'total_points', 'level', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'role'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CoachProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CoachProfile
        fields = '__all__'
        read_only_fields = ['total_formations', 'total_students', 'average_rating']


class TrainingCenterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TrainingCenterProfile
        fields = '__all__'
        read_only_fields = ['total_rooms', 'average_rating']
