from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from watchpartyserverapi.models import Member, Channel, ChannelMember

class ChannelMembers(ViewSet):
    """Request handlers for user ChannelMember info in the WatchParty Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):

        try:
            member = Member.objects.get(pk=request.data["member_id"])
        except Member.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        try:
            channel = Channel.objects.get(pk=request.data["channel_id"])
        except Channel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        channel_member = ChannelMember()
        channel_member.member = member
        channel_member.channel = channel

        try:
            channel_member.save()
            return Response({}, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                channel = Channel.objects.get(pk=pk)
            except Channel.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            members = ChannelMember.objects.filter(channel=channel)

            serializer = ChannelMemberSerializer(members, many=True, context={'request': request})
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            channel = Channel.objects.get(pk=pk)
            member = Member.objects.get(pk=request.data["member_id"])
            channel_member = ChannelMember.objects.filter(channel=channel, member=member)
            channel_member.delete()
            return Response({'message': 'member deleted'}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChannelMemberSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for channel members

    Arguments:
        serializers
    """

    class Meta:
        model = ChannelMember
        fields = ('id', 'full_name', 'profile_pic', 'member_id')
        depth = 1