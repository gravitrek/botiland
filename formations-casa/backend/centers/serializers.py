from rest_framework import serializers
from .models import TrainingCenter, Room, RoomImage, RoomAvailability, CenterReview
from accounts.serializers import UserSerializer


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'hourly_rate', 'daily_rate', 'is_active']


class TrainingCenterListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = TrainingCenter
        fields = [
            'id', 'name', 'slug', 'description', 'city', 'address',
            'owner', 'main_image', 'average_rating', 'is_approved',
            'has_parking', 'has_wifi', 'has_cafe'
        ]


class TrainingCenterDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    rooms = RoomListSerializer(many=True, read_only=True)

    class Meta:
        model = TrainingCenter
        fields = '__all__'
        read_only_fields = ['average_rating', 'total_reviews', 'is_approved', 'approved_at']


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAvailability
        fields = '__all__'


class CenterReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CenterReview
        fields = '__all__'
        read_only_fields = ['user']
