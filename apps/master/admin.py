from .models import *
from apps.master.utils.parser import generate_m3u8

from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count, QuerySet

from django_admin_multi_select_filter.filters import MultiSelectRelatedFieldListFilter
from django.utils.html import format_html


class QualitiesInline(admin.TabularInline):
    model = Quality
    extra = 1  # How many empty rows to show by default
    verbose_name = "Quality" # Changes the singular name (e.g., "Add another Item")
    verbose_name_plural = "Video Qualities"
    fields = ['quality', 'codec', 'url', 'copy_url_button'] # Optional: specify the order of fields

    readonly_fields = ("copy_url_button",)

    def copy_url_button(self, obj):
        if not obj.pk:
            return ""
        return format_html(
            '<button type="button" class="selector-chooseall" onclick="copyToClipboard(\'{}\')">Copy</button>',
            obj.url
        )

    copy_url_button.short_description = "Copy URL"

    class Media:
        js = ("admin/js/copy_clipboard.js",)

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

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
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
    inlines = [QualitiesInline]
    filter_horizontal = ('tags','performers')
    FILTER_MODEL_MAP = {"tags__id__in": Tag,"network__id__exact": Network,"performers__id__exact": Performer,}

    def tags_count(self, obj):
        return obj.tags_count

    def performers_count(self,obj):
        return obj.performers_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tags_count=Count("tags"),performers_count=Count("performers"))
        return queryset

    def export_as_HLS(self, request, queryset):
        gets = {k:v.split(',') for k,v in  request.GET.dict().items()}

        db_objects = []

        for param in self.FILTER_MODEL_MAP.keys():
            ids = gets.get(param)
            if not ids:
                continue

            model = self.FILTER_MODEL_MAP[param]
            objs = model.objects.filter(id__in=ids)

            db_objects.extend(objs)

        if db_objects:
            # print(db_objects)
            # print('-'.join(i.name for i in db_objects))
            filename = ('-'.join(i.name for i in db_objects))
        else:
            filename = "all"
        print(filename)

        m3u8File = generate_m3u8(queryset,filename)
        response = HttpResponse(m3u8File, content_type='application/x-mpegURL')

        # 3. Set the 'Content-Disposition' header to trigger a download
        # 'attachment; filename="filename.txt"' suggests the browser save it as 'filename.txt'
        response['Content-Disposition'] = f'attachment; filename="{filename}.m3u8"'

        # 4. Return the response
        return response

    tags_count.admin_order_field = 'tags_count' 
    tags_count.short_description = 'Tags Count'
    
    performers_count.admin_order_field = 'performers_count' 
    performers_count.short_description = 'Performers Count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


