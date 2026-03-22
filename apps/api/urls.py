from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, QualityViewSet, CustomTokenObtainPairView, GetItems
from rest_framework_simplejwt.views import (TokenRefreshView,)

# Initialize the router
router = DefaultRouter()

# Register our Video viewset
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'qualities', QualityViewSet, basename='quality')


urlpatterns = [
    # Include all the automatically generated DRF URLs
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('items/',GetItems.as_view(),name="get_items")
]
