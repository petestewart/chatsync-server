"""ChannelMember model"""
from django.db import models
from .channel import Channel
from .member import Member

class ChannelMember(models.Model):
    """ChannelMember model"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return f"{self.member.user.first_name} {self.member.user.last_name}"

    @property
    def profile_pic(self):
        return self.member.profile_pic
