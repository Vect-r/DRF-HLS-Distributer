from .models import *
from .forms import HLSActionForm

from apps.master.utils.parser import generate_m3u8, switcher

from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count, QuerySet
from django.shortcuts import render

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
    ordering = ['-created_at']
    actions = [
        # 'export_as_HLS',
        'export_as_hls',
        ]
    action_form = HLSActionForm
    inlines = [QualitiesInline]
    filter_horizontal = ('tags','performers')
    FILTER_MODEL_MAP = {"tags__id__in": Tag,"network__id__exact": Network,"performers__id__exact": Performer,}

    list_per_page = 20

    def tags_count(self, obj):
        return obj.tags_count

    def performers_count(self,obj):
        return obj.performers_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tags_count=Count("tags"),performers_count=Count("performers"))
        return queryset

    # def export_as_HLS(self, request, queryset):
    #     gets = {k:v.split(',') for k,v in  request.GET.dict().items()}

    #     db_objects = []

    #     for param in self.FILTER_MODEL_MAP.keys():
    #         ids = gets.get(param)
    #         if not ids:
    #             continue

    #         model = self.FILTER_MODEL_MAP[param]
    #         objs = model.objects.filter(id__in=ids)

    #         db_objects.extend(objs)

    #     if db_objects:
    #         # print(db_objects)
    #         # print('-'.join(i.name for i in db_objects))
    #         filename = ('-'.join(i.name for i in db_objects))
    #     else:
    #         filename = "all"
    #     print(filename)

    #     m3u8File = generate_m3u8(queryset,filename)
    #     response = HttpResponse(m3u8File, content_type='application/x-mpegURL')

    #     # 3. Set the 'Content-Disposition' header to trigger a download
    #     # 'attachment; filename="filename.txt"' suggests the browser save it as 'filename.txt'
    #     response['Content-Disposition'] = f'attachment; filename="{filename}.m3u8"'

    #     # 4. Return the response
    #     return response

    def get_action_choices(self, request):
        choices = super(VideoAdmin, self).get_action_choices(request)
        # choices is a list, just change it.
        # the first is the BLANK_CHOICE_DASH
        choices.pop(0)
        # do something to change the list order
        # the first one in list will be default option
        choices.reverse()
        return choices
    
    def export_as_hls(self, request, queryset):

        quality = request.POST.get("pref_quality")
        codec = request.POST.get("pref_codec")

        if not quality or not codec:
            self.message_user(request, "Please select quality and codec")
            return

        print(quality,codec)

        p={}
        qualities = list(value for value,label in Quality.QUALITY_CHOICES)
        codecs = list(value for value,label in Quality.CODECS.choices)
        

        
        self.message_user(request, f"HLS export started ({quality}, {codec})")

    export_as_hls.short_description = "Export selected videos as HLS"

    tags_count.admin_order_field = 'tags_count' 
    tags_count.short_description = 'Tags Count'
    
    performers_count.admin_order_field = 'performers_count' 
    performers_count.short_description = 'Performers Count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


