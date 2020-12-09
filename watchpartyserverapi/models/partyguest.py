"""PartyGuest model"""
from django.db import models
from .member import Member
from .party import Party

class PartyGuest(models.Model):
    """PartyGuest model"""
    guest = models.ForeignKey(Member, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    rsvp = models.BooleanField(default=True)
