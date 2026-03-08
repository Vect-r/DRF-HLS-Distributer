from .models import *
from .utils.parser import generate_m3u8

from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count

from django_admin_multi_select_filter.filters import MultiSelectRelatedFieldListFilter

# Register your models here.
@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]

@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','url','network','tags_count','performers_count')
    list_filter = (('tags', MultiSelectRelatedFieldListFilter),'network','performers',)
    search_fields = ('title','url')
    ordering = ('url','title')
    actions = ['export_as_HLS']
    filter_horizontal = ('tags','performers')

    def tags_count(self, obj):
        return obj.tags_count

    def performers_count(self,obj):
        return obj.performers_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tags_count=Count("tags"),performers_count=Count("performers"))
        return queryset

    def export_as_HLS(self, request, queryset):
        print(request.GET.dict())

    tags_count.admin_order_field = 'tags_count' 
    tags_count.short_description = 'Tags Count'
    
    performers_count.admin_order_field = 'performers_count' 
    performers_count.short_description = 'Performers Count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


