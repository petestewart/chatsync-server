"""WatchParty member model"""
from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    """WatchParty member model"""
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    bio = models.CharField(max_length=255)
    location = models.CharField(max_length=50)
    profile_pic = models.ImageField(default='avatar.jpeg', upload_to='images/avatars')
    # profile_pic = models.URLField(max_length=400)
    time_zone_offset = models.IntegerField()
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"