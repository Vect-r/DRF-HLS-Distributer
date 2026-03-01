from rest_framework import serializers
from apps.master.models import Video, Tag, Network, Performer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ['id', 'name']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    # --- READ FIELDS (Outgoing Data) ---
    network = NetworkSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    performers = ActorSerializer(many=True,read_only=True)

    # --- WRITE FIELDS (Incoming Data) ---
    network_name = serializers.CharField(write_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=255), 
        write_only=True, 
        required=False  # Because tags can be blank=True in your model
    )

    performer_names = serializers.ListField(
        child=serializers.CharField(max_length=255), 
        write_only=True, 
        required=False  # Because tags can be blank=True in your model
    )

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'url', 'created_at', 
            'performers', 'performer_names',
            'network', 'network_name',
            'tags', 'tag_names'
        ]

    def create(self, validated_data):
        # 1. Pop out the custom fields before creating the Video
        network_name = validated_data.pop('network_name')
        tag_names = validated_data.pop('tag_names', [])
        performer_names = validated_data.pop('performer_names', [])

        # 2. Get or create the Network by name
        # We strip whitespace to prevent accidental duplicates like " YouTube " vs "YouTube"
        network_obj, _ = Network.objects.get_or_create(name=network_name.strip())
        
        # 3. Create the Video instance
        video = Video.objects.create(network=network_obj, **validated_data)

        # 4. Get or create the Tags and add them to the ManyToMany field
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=name.strip())
            video.tags.add(tag_obj)

        for name in performer_names:
            performer_obj, _ = Performer.objects.get_or_create(name=name.strip())
            video.performers.add(performer_obj)



        return video

    def update(self, instance, validated_data):
        # 1. Handle Network update if provided
        if 'network_name' in validated_data:
            network_name = validated_data.pop('network_name')
            network_obj, _ = Network.objects.get_or_create(name=network_name.strip())
            instance.network = network_obj

        # 2. Handle Tags update if provided
        if 'tag_names' in validated_data:
            tag_names = validated_data.pop('tag_names')
            instance.tags.clear() # Remove old tags
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name.strip())
                instance.tags.add(tag_obj)

        # 3. Handle Actors update if provided
        if 'performer_names' in validated_data:
            performer_names = validated_data.pop('performer_names')
            instance.performers.clear() # Remove old performers
            for name in performer_names:
                performer_obj, _ = Performer.objects.get_or_create(name=name.strip())
                instance.performers.add(performer_obj)

        # 3. Update standard fields
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.save()

        return instance