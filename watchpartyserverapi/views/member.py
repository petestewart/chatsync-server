from django.http import HttpResponseServerError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from watchpartyserverapi.models import Member

class Members(ViewSet):
    """Request handlers for user Member info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, pk=None):
        """
        @api {PUT} /members/:id PUT changes to Member profile
        @apiName UpdateMember
        @apiGroup Member

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 3021ed814cfc1f5c8bb4b0ac5975c576d8c66f26

        @apiParam {id} id Member Id to update
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        member = Member.objects.get(user=request.auth.user)

        if member.id != int(pk):
            return Response('You are not authorized to update this account', status=status.HTTP_401_UNAUTHORIZED)

        try:
            member.user.first_name = request.data["first_name"]
            member.user.last_name = request.data["last_name"]
            member.user.email = request.data["email"]
            member.bio = request.data["bio"]
            member.location = request.data["location"]
            member.profile_pic = request.data["profile_pic"]
            member.time_zone_offset = request.data["time_zone_offset"]
            member.user.save()
            member.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return HttpResponseServerError(ex)