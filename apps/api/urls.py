from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Initialize the router
router = DefaultRouter()

# Register our Video viewset
router.register(r'videos', VideoViewSet, basename='video')

urlpatterns = [
    # Include all the automatically generated DRF URLs
    path('', include(router.urls)),
    path('videos/<str:category_type>/<str:name>.m3u8',m3u8_response,name="hls_response")
]
