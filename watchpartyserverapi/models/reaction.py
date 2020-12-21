"""Reaction model"""
from django.db import models

class Reaction(models.Model):
    """Reaction model"""
    name = models.CharField(max_length=25)