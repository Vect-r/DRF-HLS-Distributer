from django.contrib import admin
from .models import *
from .utils.parser import generate_m3u8
from django.http import HttpResponse
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
    # form = VideoAdminForm
    list_display = ('id','title','url','network')
    list_filter = (('tags', MultiSelectRelatedFieldListFilter),'network','performers',)
    search_fields = ('title','url')
    ordering = ('url','title')
    actions = ['export_as_m3u8']
    filter_horizontal = ('tags','performers')

    def export_as_m3u8(self, request, queryset):
        print(request.GET.dict())


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


