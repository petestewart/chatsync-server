"""Channel model"""
from django.db import models
from .member import Member

class Channel(models.Model):
    """Channel model"""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    image = models.ImageField(default='group.png', upload_to='images/channels')
    # image = models.URLField(max_length=400)
    creator = models.ForeignKey(Member, on_delete=models.CASCADE)
