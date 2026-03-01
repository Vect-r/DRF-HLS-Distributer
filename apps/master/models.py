from django.db import models
import uuid

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
    
    
class Network(BaseModel):
    name = models.CharField(max_length=255,null=False,blank=False,unique=True)

    def __str__(self):
        return self.name

class Video(BaseModel):
    title = models.CharField(max_length=255,null=False,blank=False)
    url = models.URLField(null=False,blank=False)
    tags = models.ManyToManyField(Tag, related_name='videos',blank=True)
    network = models.ForeignKey(Network,related_name="videos",on_delete=models.CASCADE)
    performers = models.ManyToManyField(Performer,related_name='videos',blank=True)


    def __str__(self):
        return f"{self.title} -> {self.network}"