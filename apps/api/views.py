from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view

from .serializers import *
from apps.master.models import *

# Create your views here.
class VideoAPI(ListAPIView):
    queryset = Video.objects.all().order_by('created_at')
    serializer_class = VideoSerializer
    # pagination_class = BlogPagination

@api_view(['GET'])
def m3u8_response(request,category_type:str,name:str):
    if category_type=="tag":
        DBObj = get_object_or_404(Tag,name=name)
    elif category_type=="network":
        DBObj = get_object_or_404(Network,name=name)
    else:
        raise Http404(f"Wrong type: {category_type}. either 'tag' or 'network")
    
    m3u8_content = """#EXTM3U
    #EXT-X-STREAM-INF:BANDWIDTH=1280000
    playlist_720.m3u8"""
    
    response = HttpResponse(m3u8_content, content_type='application/x-mpegurl')
    # Optional: Force download/save-as
    # response['Content-Disposition'] = 'attachment; filename="playlist.m3u8"'
    return response
    

    