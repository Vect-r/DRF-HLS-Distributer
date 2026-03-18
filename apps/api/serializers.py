from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from apps.master.models import Video, Tag, Network, Platform, Performer, Quality

class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quality
        fields = ['id', 'quality', 'codec', 'url']

class VideoSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(
        queryset=Platform.objects.all(),
        slug_field='name'
    )

    watch = QualitySerializer(source='qualities', many=True)

    
    network_name = serializers.CharField(write_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True,
        required=False
    )
    performer_names = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True,
        required=False
    )

    class Meta:
        model = Video
        # Notice we only list the fields that match your exact JSON keys
        fields = [
            'id','title', 'url', 'created_at','network_name', 'performer_names', 
            'platform', 'tag_names', 'watch'
        ]

    def to_representation(self, instance):
        """
        This method dictates exactly what the GET response looks like.
        We format the related models into clean string lists.
        """
        rep = super().to_representation(instance)
        
        # Build the exact dictionary structure you asked for
        return {
            "id": rep['id'],
            "title": rep['title'],
            "url": rep['url'],
            "created_at": rep['created_at'],
            "network_name": instance.network.name if instance.network else None,
            "performer_names": [perf.name for perf in instance.performers.all()],
            "platform": rep['platform'],
            "tag_names": [tag.name for tag in instance.tags.all()],
            "watch": rep['watch']
        }

    def create(self, validated_data):
        # 1. Extract dynamic fields
        network_name = validated_data.pop('network_name')
        tag_names = validated_data.pop('tag_names', [])
        performer_names = validated_data.pop('performer_names', [])
        
        qualities_data = validated_data.pop('qualities', []) 

        # 2. Get or Create Network
        network_obj, _ = Network.objects.get_or_create(name=network_name.strip())
        
        video = Video.objects.create(network=network_obj, **validated_data)

        # 4. Handle Many-to-Many Relationships
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=name.strip())
            video.tags.add(tag_obj)

        for name in performer_names:
            perf_obj, _ = Performer.objects.get_or_create(name=name.strip())
            video.performers.add(perf_obj)

        # 5. Handle Nested Qualities
        for quality_data in qualities_data:
            Quality.objects.create(video=video, **quality_data)

        return video

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        if 'platform' in validated_data:
            instance.platform = validated_data['platform']
        
        # Update Network
        if 'network_name' in validated_data:
            network_name = validated_data.pop('network_name')
            network_obj, _ = Network.objects.get_or_create(name=network_name.strip())
            instance.network = network_obj

        # Update Tags
        if 'tag_names' in validated_data:
            instance.tags.clear()
            for name in validated_data.pop('tag_names'):
                tag_obj, _ = Tag.objects.get_or_create(name=name.strip())
                instance.tags.add(tag_obj)

        # Update Performers
        if 'performer_names' in validated_data:
            instance.performers.clear()
            for name in validated_data.pop('performer_names'):
                perf_obj, _ = Performer.objects.get_or_create(name=name.strip())
                instance.performers.add(perf_obj)

        if 'qualities' in validated_data:
            qualities_data = validated_data.pop('qualities')
            
            for quality_data in qualities_data:
                Quality.objects.update_or_create(
                    video=instance,
                    quality=quality_data.get('quality'),
                    codec=quality_data.get('codec'),
                    defaults={
                        'url': quality_data.get('url')
                    }
                )

        instance.save()
        return instance
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        last_login_epoch = int(user.last_login.timestamp()) if user.last_login else None
        
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['last_login'] = last_login_epoch
        return token

# Connect the custom serializer to a new View
