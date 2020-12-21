from django.db.models import fields
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from watchpartyserverapi.models import Reaction


class Reactions(ViewSet):
    """Request handlers for Reactions info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """GET all reactions"""
        try:
            reactions = Reaction.objects.all()
            serializer = ReactionSerializer(reactions, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """GET single reaction"""
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class ReactionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for reaction

    Arguments:
        serializers
    """
    class Meta:
        model = Reaction
        url = serializers.HyperlinkedIdentityField(
            view_name='reactions',
            lookup_field='id'
        )
        fields = ('id', 'name', 'url')
        depth = 1