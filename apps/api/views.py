from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from rest_framework import viewsets, filters, mixins, status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .filters import *
from .pagination import CustomLimitOffsetPagination
from apps.master.models import *
from apps.master.utils.parser import generate_m3u8, qualities, codecs

# Create your views here.

# @api_view(['GET'])
# def get_items(request):
    

class GetItems(APIView):
    """
    View to list all users in the system.
    * Requires Token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        data={
            'qualities':qualities,
            'codecs':codecs,
        }
        data['tags'] = Tag.objects.all().values_list('name',flat=True)
        data['performers'] = Performer.objects.all().values_list('name',flat=True)
        data['platforms'] = Platform.objects.all().values_list('name',flat=True)
        data['networks'] = Network.objects.all().values_list('name',flat=True)
        return Response(data)

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter ]
    filterset_class = VideoFilter
    # filterset_fields = ['network', 'tags__name']
    search_fields = ['title', 'url','network__name']
    filter_list = ['tag','network','performer']
    permission_classes = [IsAuthenticated]
    ordering_fields = ['title','network__name','created_at',]
    ordering = ['-created_at']
    pagination_class = CustomLimitOffsetPagination

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
    permission_classes = [IsAuthenticated]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer