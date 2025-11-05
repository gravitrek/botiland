from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import TrainingCenter, Room, RoomAvailability
from .serializers import (
    TrainingCenterListSerializer, TrainingCenterDetailSerializer,
    RoomSerializer, RoomAvailabilitySerializer
)


class TrainingCenterViewSet(viewsets.ModelViewSet):
    queryset = TrainingCenter.objects.filter(is_approved=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'has_parking', 'has_wifi']
    search_fields = ['name', 'description', 'address']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return TrainingCenterListSerializer
        return TrainingCenterDetailSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.filter(is_active=True)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['training_center', 'layout_type']


class RoomAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = RoomAvailability.objects.all()
    serializer_class = RoomAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room', 'date', 'is_available']
