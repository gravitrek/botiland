from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, FormationType, Formation, FormationReview
from .serializers import (
    CategorySerializer, FormationTypeSerializer,
    FormationListSerializer, FormationDetailSerializer,
    FormationCreateSerializer, FormationReviewSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class FormationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FormationType.objects.all()
    serializer_class = FormationTypeSerializer
    permission_classes = [permissions.AllowAny]


class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'delivery_mode', 'level', 'status']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['start_date', 'price', 'average_rating', 'created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return FormationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FormationCreateSerializer
        return FormationDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Only show published formations to non-owners
        if self.request.user.is_authenticated:
            if self.request.user.role == 'coach':
                queryset = queryset.filter(
                    coach=self.request.user
                ) | queryset.filter(status='published')
        else:
            queryset = queryset.filter(status='published')
        return queryset

    @action(detail=True, methods=['post'])
    def enroll(self, request, slug=None):
        """Enroll in a formation"""
        formation = self.get_object()
        # This would create a booking - implement in bookings app
        return Response({'message': 'Enrollment successful'})

    @action(detail=False, methods=['get'])
    def my_formations(self, request):
        """Get formations created by current user"""
        formations = self.queryset.filter(coach=request.user)
        serializer = FormationListSerializer(formations, many=True)
        return Response(serializer.data)


class FormationReviewViewSet(viewsets.ModelViewSet):
    queryset = FormationReview.objects.all()
    serializer_class = FormationReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['formation', 'user', 'rating']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
