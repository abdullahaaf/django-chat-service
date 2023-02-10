import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.http import Http404
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Message,ChatRooms

from .serializers import MessageSerializer, ChatRoomSerializer

class MessageHandler(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get_specific_text_message(self, timestamp):
        try:
            return Message.objects.get(timestamp=timestamp)
        except Message.DoesNotExist:
            raise Http404

    def save_chat_room(self, data):
        sender = self.get_user(data['sender'])
        receiver = self.get_user(data['receiver'])

        check_user_as_sender = ChatRooms.objects.filter(sender = sender.id).filter(receiver=receiver.id)
        check_user_as_receiver = ChatRooms.objects.filter(sender = receiver.id).filter(receiver=sender.id)

        serializer = ChatRoomSerializer(data=data)
        if serializer.is_valid() and (check_user_as_sender.exists() == False and check_user_as_receiver.exists() == False):
            serializer.save()

    def get(self, request):
        user = self.get_user(request.user.username)
        partner = self.get_user(request.GET['partner'])

        messages = Message.objects.filter(
            (Q(sender=user.id) & Q(receiver=partner)) |
            (Q(sender=partner) & Q(receiver=user.id))
        )

        my_unread_messages = Message.objects.filter(Q(sender=partner) & Q(receiver=user.id))
        for message in my_unread_messages:
            message.is_read = True
            message.save()

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        current_unix_timestamp = int(round(time.time() * 1000))
        if request.data.get('replied_timestamp') == None:
            previous = None
        else:
            previous = self.get_specific_text_message(request.data.get('replied_timestamp'))
            previous = previous.id

        message_data = {
            'sender': request.user.username,
            'receiver': self.get_user(request.data.get('receiver')),
            'message' : request.data.get('message'),
            'timestamp' : current_unix_timestamp,
            'previous' : previous
        }

        serializer = MessageSerializer(data=message_data)

        if serializer.is_valid():
            self.save_chat_room(message_data)
            serializer.save()

            return Response({
                "message": "Success sent message",
                "data" : serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ChatRoomList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        chat_rooms = ChatRooms.objects.filter(Q(sender=request.user.id) | Q(receiver=request.user.id))
        serializer = ChatRoomSerializer(chat_rooms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)