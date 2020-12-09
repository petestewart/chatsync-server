"""View module for handling requests about member profiles"""
import datetime
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from watchpartyserverapi.models import Member

class Profile(ViewSet):
    """Request handlers for user profile info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """
        @api {GET} /profile GET user profile info
        @apiName GetProfile
        @apiGroup UserProfile

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiSuccess (200) {Number} id Profile id
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
                "id": 7,
                "url": "http://localhost:8000/members/7",
                "user": {
                    "first_name": "Pete",
                    "last_name": "Stewart",
                    "email": "pete@example.com"
                },
                "bio": "Just here to have fun",
                "location": "Nashville, TN",
                "profile_pic": "http://example.com/pic.jpg",
                "location": "Nashville, TN",
                "time_zone_offset": -6
            }
        """
        try:
            current_user = Member.objects.get(user=request.auth.user)
            serializer = ProfileSerializer(current_user, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for member profile

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        depth = 1

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for member profile

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Member
        # url = serializers.HyperlinkedIdentityField(
        #     view_name='member',
        #     lookup_field='id'
        # )
        fields = ('id', 'user', 'bio', 'location', 'profile_pic', 'location', 'time_zone_offset')
        depth = 1