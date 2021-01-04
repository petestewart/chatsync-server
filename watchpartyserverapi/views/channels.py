import uuid
import base64
from django.http import HttpResponseServerError
# from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from django.core.files.base import ContentFile
from watchpartyserverapi.models import Member, Channel, ChannelMember

class Channels(ViewSet):
    """Request handles for Channel info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def create(self, request):
        """
        Create Channel viewset
        """
        current_user = Member.objects.get(user=request.auth.user)
        new_channel = Channel()
        new_channel.name = request.data["name"]
        new_channel.description = request.data["description"]
        # new_channel.image = request.data["image"]
        new_channel.creator = current_user

        if request.data["image"] is not None:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'"image"-{uuid.uuid4()}.{ext}')
            new_channel.image = data
        else: new_channel.image = ""

        try:
            new_channel.save()
            new_channel.members=[]
            serializer = ChannelSerializer(new_channel, many=False, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        Update Channel viewset
        """

        channel = Channel.objects.get(pk=pk)
        channel.name = request.data["name"]
        channel.description = request.data["description"]

        # channel.image = request.data["image"]

        if request.data["image"] is not None:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'"image"-{uuid.uuid4()}.{ext}')
            channel.image = data

        try:
            channel.save()
            channel.members=[]
            serializer = ChannelSerializer(channel, many=False, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """GET for all channels"""
        try:
            channels = Channel.objects.all()


            # Filter by member if requested
            member_id = self.request.query_params.get('member_id', None)

            if member_id is not None:
                channels = []
                member = Member.objects.get(pk=member_id)
                member_channels = ChannelMember.objects.filter(member=member)
                for chan in member_channels:
                    channel = Channel.objects.get(pk=chan.channel.id)
                    channels.append(channel)

            for channel in channels:
                members = ChannelMember.objects.filter(channel=channel)
                channel.members = members

            # # Filter by member if requested
            # member_id = self.request.query_params.get('member_id', None)

            # if member_id is not None:
            #     member = Member.objects.get(pk=member_id)
            #     channels = channels.filter(member=member)

            serializer = ChannelSerializer(channels, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """GET for single channel"""
        try:
            channel = Channel.objects.get(pk=pk)

            members = ChannelMember.objects.filter(channel=channel)
            channel.members = members

            serializer = ChannelSerializer(channel, many=False, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """DELETE single channel"""
        try:
            channel = Channel.objects.get(pk=pk)

        except Channel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        try:
            channel.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return HttpResponseServerError(ex)



class MemberSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for member profile

    Arguments:
        serializers
    """
    class Meta:
        model = Member
        fields = ('id', 'full_name')
        # fields = ('id', 'full_name', 'profile_pic')
        depth = 1

class ChannelMemberSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for channel members

    Arguments:
        serializers
    """

    profile_pic = serializers.ImageField()

    class Meta:
        model = ChannelMember
        # fields = ('full_name', 'member_id')
        fields = ('full_name', 'profile_pic', 'member_id')
        depth = 1


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for channel profile

    Arguments:
        serializers
    """

    creator = MemberSerializer(many=False)
    members = ChannelMemberSerializer(many=True)

    class Meta:
        model = Channel
        url = serializers.HyperlinkedIdentityField(
            view_name='channels',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'description', 'image', 'creator', 'members')
        depth = 1
