from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, QualityViewSet

# Initialize the router
router = DefaultRouter()

# Register our Video viewset
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'qualities', QualityViewSet, basename='quality')

urlpatterns = [
    # Include all the automatically generated DRF URLs
    path('', include(router.urls)),
]
