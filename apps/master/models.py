from django.db import models
import uuid
from django.db.models import UniqueConstraint

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tag(BaseModel):
    name = models.CharField(max_length=255,null=False,blank=False,unique=True)

    def __str__(self):
        return self.name

class Performer(BaseModel):
    name = models.CharField(max_length=255,null=False,blank=False,unique=True)

    def __str__(self):
        return self.name
    
class Platform(BaseModel):
    name = models.CharField(max_length=255,null=False,blank=False,unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name
    
    
class Network(BaseModel):
    name = models.CharField(max_length=255,null=False,blank=False,unique=True)

    def __str__(self):
        return self.name

class Video(BaseModel):
    title = models.CharField(max_length=255,null=False,blank=False)
    url = models.URLField(null=False,blank=False,unique=True)
    tags = models.ManyToManyField(Tag, related_name='videos',blank=True)
    network = models.ForeignKey(Network,related_name="videos",on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform,related_name='videos',on_delete=models.CASCADE)
    performers = models.ManyToManyField(Performer,related_name='videos',blank=True)

    def __str__(self):
        return f"{self.title} -> {self.network}"
    
class Quality(BaseModel):
    class CODECS(models.TextChoices):
        AV1 = "av1", "AV1"
        H264 = "h264", "H264"

    QUALITY_CHOICES = [
        ('240p', '240p (SD)'),
        ('360p', '360p (SD)'),
        ('480p', '480p (SD)'),
        ('720p', '720p (HD)'),
        ('1080p', '1080p (Full HD)'),
        ('1440p', '1440p (Quad HD)'),
        ('2160p', '4K (UHD)'),
    ]

    # Your fields
    video = models.ForeignKey(Video, related_name="qualities", on_delete=models.CASCADE)
    quality = models.CharField(choices=QUALITY_CHOICES, max_length=10)
    codec = models.CharField(choices=CODECS.choices, max_length=10)
    url = models.URLField(null=False, blank=False)

    class Meta:
        # Ensures a video can't have duplicate qualities for the same codec
        constraints = [
            UniqueConstraint(
                fields=['video', 'quality', 'codec'], 
                name='unique_video_quality_codec'
            )
        ]

    def __str__(self):
        return f"{self.video.title} - {self.get_quality_display()} ({self.codec})"