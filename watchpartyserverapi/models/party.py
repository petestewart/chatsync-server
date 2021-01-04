"""Party model"""
from django.db import models
from .channel import Channel
from .member import Member

class Party(models.Model):
    """Party model"""
    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(Member, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    datetime_end = models.DateTimeField(auto_now=False, auto_now_add=False)
    description = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    title = models.CharField(max_length=50)
