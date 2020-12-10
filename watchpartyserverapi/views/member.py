from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from watchpartyserverapi.models import Member

class Members(ViewSet):
    """Request handlers for user Member info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def retrieve(self, request, pk=None):
        """
        @api {GET} /members GET user member profile info
        @apiName GetMemberProfile
        @apiGroup UserMemberProfile

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
                "time_zone_offset": -6
            }
        """
        current_user = Member.objects.get(user=request.auth.user)
        if pk == "me":
            serializer = ProfileSerializer(current_user, many=False, context={'request': request})
            return Response(serializer.data)

        try:
            user = Member.objects.get(pk=pk)
            serializer = ProfileSerializer(user, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """
        @api {GET} /members GET all user members profile info
        @apiName GetMemberProfiles
        @apiGroup UserMemberProfiles

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
                "time_zone_offset": -6
            },
            ...
        """
        try:
            users = Member.objects.all()

            serializer = ProfileSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex)

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
            current_user = Member.objects.get(user=request.auth.user)
            serializer = ProfileSerializer(current_user, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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