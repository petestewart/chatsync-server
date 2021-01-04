from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from watchpartyserverapi.models import Channel, Member, Party, PartyGuest
from datetime import datetime

class Parties(ViewSet):
    """Request handlers for user Party info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """
            @api {POST} /parties POST new party
            @apiName CreateParty
            @apiGroup Parties

            @apiHeader {String} Authorization Auth token
            @apiHeaderExample {String} Authorization
                Token 9ba45f09651c5b0c404f37a2d2572c026c146611

            @apiParam {String} name Short form name of party
            @apiParam {Number} price Cost of party
            @apiParam {String} description Long form description of party
            @apiParam {String} location City where party is located
            @apiParam {Number} category_id Category of party
            @apiParamExample {json} Input
                {
                    "title": "MLS Cup",
                    "description": "Sounders vs Crew",
                    "datetime": "2020-12-11 23:30",
                    "is_public" : false
                }

            @apiSuccess (200) {Object} party Created party
            @apiSuccess (200) {id} party.id party Id
            @apiSuccess (200) {String} party.title Short form title of party
            @apiSuccess (200) {String} party.description Long form description of party
            @apiSuccess (200) {Object} party.creator Created Party
            @apiSuccess (200) {Date} party.datetime Date and time of party
            @apiSuccess (200) {Boolean} party.isPublic Status of party's privacy
            @apiSuccessExample {json} Success
                HTTP/1.1 200 OK
                {
                    "id": 1,
                    "title": "MLS Cup",
                    "datetime": "2020-12-11T23:30:00Z",
                    "description": "Sounders vs Crew",
                    "is_public": false,
                    "creator": {
                        "id": 1,
                        "user": {
                            "first_name": "Pete",
                            "last_name": "Stewart"
                        }
                    }
                }
        """
        current_user = Member.objects.get(user=request.auth.user)
        channel = None

        new_party = Party()
        new_party.creator = current_user
        new_party.title = request.data["title"]
        new_party.description = request.data["description"]
        new_party.datetime = request.data["datetime"]
        new_party.datetime_end = request.data["datetime_end"]
        new_party.is_public = request.data["is_public"]

        channel_id = request.data["channel_id"]

        if channel_id is not None:
            try:
                channel = Channel.objects.get(pk=channel_id)

            except Channel.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

        new_party.channel = channel

        partyguest = PartyGuest()
        partyguest.guest = current_user
        partyguest.party = new_party
        partyguest.rsvp = True

        try:
            new_party.save()
            partyguest.save()
            partyguests = PartyGuest.objects.filter(party=new_party)
            new_party.guests = partyguests
            serializer = PartySerializer(new_party, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
            @api {PUT} /parties/:id  update existing party
            @apiName UpdateParty
            @apiGroup Parties

            @apiParam {id} Party Id to update

            @apiHeader {String} Authorization Auth token
            @apiHeaderExample {String} Authorization
                Token 9ba45f09651c5b0c404f37a2d2572c026c146611

            @apiParam {String} name Short form name of party
            @apiParam {Number} price Cost of party
            @apiParam {String} description Long form description of party
            @apiParam {Number} quantity Number of items to sell
            @apiParam {String} location City where party is located
            @apiParam {Number} category_id Category of party
            @apiParamExample {json} Input
                {
                    "title": "MLS Cup",
                    "description": "Sounders vs Crew",
                    "datetime": "2020-12-11 23:30",
                    "is_public" : false
                }

            @apiSuccess (200) {Object} party Created party
            @apiSuccess (200) {id} party.id party Id
            @apiSuccess (200) {String} party.title Short form title of party
            @apiSuccess (200) {String} party.description Long form description of party
            @apiSuccess (200) {Object} party.creator Created party
            @apiSuccess (200) {Date} party.datetime Date and time of party
            @apiSuccess (200) {Boolean} party.isPublic Status of party's privacy
            @apiSuccessExample {json} Success
                HTTP/1.1 200 OK
                {
                    "id": 1,
                    "title": "MLS Cup",
                    "datetime": "2020-12-11T23:30:00Z",
                    "description": "Sounders vs Crew",
                    "is_public": false,
                    "creator": {
                        "id": 1,
                        "user": {
                            "first_name": "Pete",
                            "last_name": "Stewart"
                        }
                    }
                }
        """

        party = Party.objects.get(pk=pk)
        party.title = request.data["title"]
        party.description = request.data["description"]
        party.datetime = request.data["datetime"]
        party.datetime_end = request.data["datetime_end"]
        party.is_public = request.data["is_public"]

        channel_id = request.data["channel_id"]
        if channel_id is not None:
            try:
                channel = Channel.objects.get(pk=request.data["channel_id"])
                party.channel = channel
            except Channel.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        else:
            party.channel = None

        try:
            party.save()
            partyguests = PartyGuest.objects.filter(party = party)
            party.guests = partyguests
            serializer = PartySerializer(party, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """
            @api {GET} /party/{partyId} GET Party info
            @apiName GetParty
            @apiGroup Parties

            @apiHeader {String} Authorization Auth token
            @apiHeaderExample {String} Authorization
                Token 9ba45f09651c5b0c404f37a2d2572c026c146611

            @apiSuccess (200) {Number} id Member id
            @apiSuccess (200) {String} url URI of Member profile
            @apiSuccess (200) {Object} user Related user object
            @apiSuccess (200) {String} user.first_name Member first name
            @apiSuccess (200) {String} user.last_name Member last name
            @apiSuccess (200) {String} user.email Member email
            @apiSuccess (200) {String} bio Member bio
            @apiSuccess (200) {String} location Member location
            @apiSuccess (200) {String} profile_pic Member profile pic URL
            @apiSuccess (200) {String} time_zone_offset Member time zone (hours offset to UTC)

            @apiSuccessExample {json} Success
                HTTP/1.1 200 OK
                {
                    "id": 1,
                    "url": "http://localhost:8000/parties/1",
                    "creator": {
                        "first_name": "Pete",
                        "last_name": "Stewart",
                        "email": "pete@example.com"
                    },
                    "title": "MLS Cup",
                    "description": "Sounders vs Crew",
                    "datetime": "10/25/2006 14:30"
                    "isPublic" : false
                }
        """
        try:
            party = Party.objects.get(pk=pk)
            partyguests = PartyGuest.objects.filter(party = party)
            
            guests = []
            for partyguest in partyguests:
                guest = partyguest.guest
                guests.append(guest)
            party.guests = guests
            
            serializer = PartySerializer(party, many=False, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """
            @api {DELETE} /parties/:id DELETE party
            @apiName DeleteParty
            @apiGroup Parties

            @apiParam {id} Party Id to delete

            @apiHeader {String} Authorization Auth token
            @apiHeaderExample {String} Authorization
                Token 9ba45f09651c5b0c404f37a2d2572c026c146611

            @apiSuccessExample {json} Success
                HTTP/1.1 204 No Content
        """

        current_user = Member.objects.get(user=request.auth.user)

        try:
            party = Party.objects.get(pk=pk)

        except Party.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        if party.creator != current_user:
            return Response({'message': 'Unauthorized to delete party'}, status=status.HTTP_401_UNAUTHORIZED)

        party.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        try:
            parties = Party.objects.all()

            # filter by channel if requested
            channel_id = self.request.query_params.get('channel_id', None)

            if channel_id is not None:
                channel = Channel.objects.get(pk=channel_id)
                parties = parties.filter(channel=channel)

            for party in parties:
                partyguests = PartyGuest.objects.filter(party = party)
                guests = []
                for partyguest in partyguests:
                    guest = partyguest.guest
                    guests.append(guest)
                party.guests = guests

            serializer = PartySerializer(parties, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=['get'], detail=False)
    def myupcoming(self, request):
        """
        returns all upcoming parties I am a guest for
        """
        try:
            member = Member.objects.get(user=request.auth.user)
            invites = PartyGuest.objects.filter(guest=member)
            parties = []

            for invite in invites:
                party = invite.party
                if party not in parties and party.datetime_end >= datetime.now():
                # if party not in parties:
                    parties.append(party)

            for party in parties:
                partyguest = PartyGuest.objects.filter(party=party, guest=member).first()
                party.rsvp = partyguest.rsvp

            serializer = PartyWithRSVPSerializer(parties, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for channel profile

    Arguments:
        serializers
    """

    image = serializers.ImageField()

    class Meta:
        model = Channel
        url = serializers.HyperlinkedIdentityField(
            view_name='channels',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'image')
        depth = 0


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for member profile

    Arguments:
        serializers
    """

    profile_pic = serializers.ImageField()

    class Meta:
        model = Member
        fields = ('id', 'full_name', 'profile_pic')
        depth = 1

class PartySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for member profile

    Arguments:
        serializers
    """
    channel = ChannelSerializer(many=False)
    creator = MemberSerializer(many=False)
    guests = MemberSerializer(many=True)

    class Meta:
        model = Party
        url = serializers.HyperlinkedIdentityField(
            view_name='parties',
            lookup_field='id'
        )
        fields = ('id', 'url', 'guests', 'title', 'datetime', 'datetime_end', 'description', 'is_public', 'creator', 'channel')
        depth = 1

class RSVPSerializer(serializers.BooleanField):
    """JSON serializer for RSVP on Party Guest"""
    fields = ('rsvp')
    depth = 0


class PartyWithRSVPSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for member profile

    Arguments:
        serializers
    """
    creator = MemberSerializer(many=False)
    # guests = MemberSerializer(many=True)
    rsvp = RSVPSerializer()
    class Meta:
        model = Party
        url = serializers.HyperlinkedIdentityField(
            view_name='parties',
            lookup_field='id'
        )
        fields = ('id', 'url', 'rsvp', 'title', 'datetime', 'datetime_end', 'description', 'is_public', 'creator', 'channel')
        depth = 1
