from django.db.models import fields
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.fields import IntegerField
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from watchpartyserverapi.models import MessageReaction, Reaction, Member, Party


class MessageReactions(ViewSet):
    """Request handlers for MessageReactions info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """GET message reactions, optionally by message or by party"""
        message_reactions = MessageReaction.objects.all()

        # Filter by message or party if requested
        message_id = self.request.query_params.get('message_id', None)
        party = self.request.query_params.get('party', None)

        if party is not None:
            message_reactions = message_reactions.filter(party=party)

        if message_id is not None:
            message_reactions = message_reactions.filter(message_id=message_id)

        try:
            serializer = MessageReactionSerializer(message_reactions, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
                return HttpResponseServerError(ex)

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for member profile

    Arguments:
        serializers
    """

    class Meta:
        model = Member
        # url = serializers.HyperlinkedIdentityField(
        #     view_name='members',
        #     lookup_field='id'
        # )
        fields = ('id', 'full_name')
        depth = 1

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

class PartySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Party

    Arguments:
        serializers
    """
    class Meta:
        model = Party
        url = serializers.HyperlinkedIdentityField(
            view_name='reactions',
            lookup_field='id'
        )
        fields = ('id', 'url')
        depth = 1

class MessageReactionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for reaction

    Arguments:
        serializers
    """

    party = PartySerializer(many=False)
    reaction = ReactionSerializer(many=False)
    reactor = MemberSerializer(many=False)

    class Meta:
        model = MessageReaction
        fields = ('id', 'reaction', 'reactor', 'message_id', 'party')
        depth = 1