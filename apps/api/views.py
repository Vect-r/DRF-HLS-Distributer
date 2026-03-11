from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .filters import *
from apps.master.models import *
from apps.master.utils.parser import generate_m3u8

# Create your views here.
class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all().order_by('created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = VideoFilter
    # filterset_fields = ['network', 'tags__name']
    search_fields = ['title', 'url']
    filter_list = ['tag','network','performer']

    def list(self, request, *args, **kwargs):
        # 1. Catch the custom 'download' query parameter
        is_download = request.query_params.get('download', '').lower() == 'true'

        if is_download:
            queryset = self.filter_queryset(self.get_queryset())

            active_filters = []

            for filter in self.filter_list:
                params = request.query_params.getlist(filter, [])  
                active_filters.extend(params)


            if active_filters:
                filter_string = "_".join(active_filters)
                filter_string = filter_string.replace(" ", "_")
                filename = f"{filter_string}_videos"
            else:
                filename = "all_videos"
            
            hls_file = generate_m3u8(queryset,filename)
            response = HttpResponse(hls_file,content_type='application/x-mpegURL')
            response['Content-Disposition'] = f'attachment; filename="{filename}.m3u8"'
            return response

        return super().list(request, *args, **kwargs)

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
    

    