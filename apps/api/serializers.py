from apps.master.models import *
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ['name']

class VideoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    network = NetworkSerializer()
    class Meta:
        model = Video
        fields = ['title','url','network','tags']

