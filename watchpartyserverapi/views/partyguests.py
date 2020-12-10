from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from watchpartyserverapi.models import Member, Party, PartyGuest

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
            return Response({}, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
