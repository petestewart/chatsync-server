"""MessageReaction model"""
from django.db import models
from .member import Member
from .party import Party
from .reaction import Reaction

class MessageReaction(models.Model):
    """MessageReaction model"""
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    message_id = models.CharField(max_length=255)
    reactor = models.ForeignKey(Member, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
