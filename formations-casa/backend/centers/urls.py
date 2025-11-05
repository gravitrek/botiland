from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingCenterViewSet, RoomViewSet, RoomAvailabilityViewSet

router = DefaultRouter()
router.register(r'centers', TrainingCenterViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'availability', RoomAvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
