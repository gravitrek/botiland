from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    FormationTypeViewSet,
    FormationViewSet,
    FormationReviewViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"types", FormationTypeViewSet)
router.register(r"formations", FormationViewSet)
router.register(r"reviews", FormationReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
