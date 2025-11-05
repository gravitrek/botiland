from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CoachProfileViewSet, TrainingCenterProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'coach-profiles', CoachProfileViewSet)
router.register(r'center-profiles', TrainingCenterProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
