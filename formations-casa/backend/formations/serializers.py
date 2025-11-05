from rest_framework import serializers
from .models import Category, FormationType, Formation, Curriculum, FormationReview
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FormationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormationType
        fields = '__all__'


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'


class FormationListSerializer(serializers.ModelSerializer):
    coach = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Formation
        fields = [
            'id', 'title', 'slug', 'short_description', 'coach',
            'category', 'level', 'cover_image', 'delivery_mode',
            'start_date', 'end_date', 'duration_hours', 'price',
            'currency', 'max_participants', 'current_participants',
            'average_rating', 'status', 'is_featured'
        ]


class FormationDetailSerializer(serializers.ModelSerializer):
    coach = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    formation_type = FormationTypeSerializer(read_only=True)
    curriculum_items = CurriculumSerializer(many=True, read_only=True)

    class Meta:
        model = Formation
        fields = '__all__'
        read_only_fields = ['views_count', 'average_rating', 'total_ratings', 'current_participants']


class FormationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        exclude = ['coach', 'views_count', 'average_rating', 'total_ratings', 'current_participants']

    def create(self, validated_data):
        validated_data['coach'] = self.context['request'].user
        return super().create(validated_data)


class FormationReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = FormationReview
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
