from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from watchpartyserverapi.models import Member, Party, PartyGuest

from watchpartyserverapi.firebase.firebase import send_notification


class PartyGuests(ViewSet):
    """Request handlers for user PartyGuest info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """
            @api {POST} /partyguests POST new party
            @apiName CreatePartyGuest
            @apiGroup PartyGuests

            @apiHeader {String} Authorization Auth token
            @apiHeaderExample {String} Authorization
                Token 9ba45f09651c5b0c404f37a2d2572c026c146611

            @apiParam {Number} PartyId
            @apiParam {Number} MemberId of Guest
            @apiParamExample {json} Input
                {
                    "guest_id": 1,
                    "party_id": 1,
                    "rsvp": false
                }

            @apiSuccess (200) {Object} party Created PartyGuest
            @apiSuccessExample {json} Success
                HTTP/1.1 200 OK
        """

        try:
            guest = Member.objects.get(pk=request.data["guest_id"])
        except Member.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        try:
            party = Party.objects.get(pk=request.data["party_id"])
        except Party.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        party_guest = PartyGuest()
        party_guest.guest = guest
        party_guest.party = party
        party_guest.rsvp = request.data["rsvp"]

        try:
            party_guest.save()

            if party.title is not '':
                message = f"You have been invited to the event {party.title}!"
            else:
                message = "You have been invited to an event!"

            recipient = f"{guest.id}"
            link = f"/party/{party.id}"
            send_notification(recipient, message, link)

            return Response({}, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                party = Party.objects.get(pk=pk)
            except Party.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            guests = PartyGuest.objects.filter(party=party)

            serializer = PartyGuestSerializer(guests, many=True, context={'request': request})
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            party = Party.objects.get(pk=pk)
            guest = Member.objects.get(pk=request.data["guest_id"])
            party_guest = PartyGuest.objects.get(party=party, guest=guest)
            party_guest.delete()
            return Response({'message': 'guest deleted'}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class PartyGuestSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for party guests

    Arguments:
        serializers
    """

    profile_pic = serializers.ImageField()

    class Meta:
        model = PartyGuest
        fields = ('id', 'full_name', 'profile_pic', 'guest_id', 'rsvp')
        depth = 1