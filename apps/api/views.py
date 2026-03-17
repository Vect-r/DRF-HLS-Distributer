from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from rest_framework import viewsets, filters, mixins, status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .filters import *
from apps.master.models import *
from apps.master.utils.parser import generate_m3u8, qualities, codecs

# Create your views here.

@api_view(['GET'])
def get_items(request):
    data={}
    data['tags'] = Tag.objects.all().values_list('name',flat=True)
    data['performers'] = Performer.objects.all().values_list('name',flat=True)
    data['platforms'] = Platform.objects.all().values_list('name',flat=True)
    data['networks'] = Network.objects.all().values_list('name',flat=True)
    return Response(data)

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all().order_by('created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = VideoFilter
    # filterset_fields = ['network', 'tags__name']
    search_fields = ['title', 'url']
    filter_list = ['tag','network','performer']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        # 1. Catch the custom 'download' query parameter
        is_download = request.query_params.get('download', '').lower() == 'true'
        quality = request.query_params.get('quality', '').lower()
        codec = request.query_params.get('codec', '').lower()
        
        # preferred_quality = request.query_params.get()
        print(quality)

        if is_download:
            if not quality:
                return Response({"error":f"quality is required"},status=status.HTTP_400_BAD_REQUEST)

            if quality not in qualities:
                return Response({"error":f"{quality} is not valid quality."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            if not codec:
                return Response({"error":f"codec is required"},status=status.HTTP_400_BAD_REQUEST)

            if codec not in codecs:
                return Response({"error":f"{codec} is not valid codec."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            

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
            
            hls_file = generate_m3u8(queryset,filename,codec,quality)
            response = HttpResponse(hls_file,content_type='application/x-mpegURL')
            response['Content-Disposition'] = f'attachment; filename="{filename}.m3u8"'
            return response

        return super().list(request, *args, **kwargs)
    
class QualityViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Quality.objects.all()
    serializer_class = QualitySerializer    
    permission_classes = [IsAuthenticatedOrReadOnly]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer