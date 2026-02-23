from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title','url','network')
    list_filter = ('tags','network')
    search_fields = ('title','url')
    ordering = ('url','title')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


