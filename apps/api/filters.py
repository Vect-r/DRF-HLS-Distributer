import django_filters
from apps.master.models import Video

class VideoFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name="tags__name",lookup_expr='iexact')
    network = django_filters.CharFilter(field_name="network__name",lookup_expr='iexact')

    class Meta:
        model = Video
        fields = ['tag','network']