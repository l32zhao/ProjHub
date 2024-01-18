from django.db import models
import uuid

from users.models import Profile

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    
    title = models.CharField(max_length=200)    # Required Field
    description = models.TextField(null=True, blank=True)   # Allow empty
    
    # Image
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    
    # Link
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    
    # Many-to-many Relationship
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    # Key
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False) # 16-char string
    
    def __str__(self) -> str:
        return self.title
    
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # owner = 
    
    # One-to-many Relationship
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # will be deleted if project deleted
    
    body = models.TextField(null=True, blank=True)   # Allow empty
    value = models.CharField(max_length=200, choices=VOTE_TYPE)    # Required Field
    created = models.DateTimeField(auto_now_add=True)
    
    # Key
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False) # 16-char string
    
    def __str__(self) -> str:
        return self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
    # Key
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False) # 16-char string
    
    def __str__(self) -> str:
        return self.name