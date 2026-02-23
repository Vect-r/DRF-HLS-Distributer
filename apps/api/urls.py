from django.urls import path
from .views import *

urlpatterns = [
    path('videos/',VideoAPI.as_view(),name='video_api'),
    path('videos/<str:category_type>/<str:name>.m3u8',m3u8_response,name="hls_response")
]
