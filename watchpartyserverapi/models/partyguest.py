"""PartyGuest model"""
from django.db import models
from .member import Member
from .party import Party

class PartyGuest(models.Model):
    """PartyGuest model"""
    guest = models.ForeignKey(Member, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    rsvp = models.BooleanField(default=True)

    @property
    def full_name(self):
        return f"{self.guest.user.first_name} {self.guest.user.last_name}"

    @property
    def profile_pic(self):
        return self.guest.profile_pic

    @property
    def member_id(self):
        return self.guest.id
