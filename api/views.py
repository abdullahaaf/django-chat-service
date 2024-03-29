import time

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from django.db.models import Q
from django.contrib.auth.models import User

from .models import Message,ChatRooms
from .serializers import MessageSerializer, ChatRoomSerializer
from .response_helper import response_success, response_error

class RegisterApi(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = User.objects.create_user(
            username=request.data.get('username'),
            email=request.data.get('email'),
            password=request.data.get('password')
        )
        user.save()
        request.data.pop('password')

        return response_success("success register", request.data, status.HTTP_201_CREATED)

class MessageHandler(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return response_success("user isn't exist",{},status.HTTP_204_NO_CONTENT)

    def get_specific_text_message(self, timestamp):
        try:
            return Message.objects.get(timestamp=timestamp)
        except Message.DoesNotExist:
            return response_success("message isn't exist",{},status.HTTP_204_NO_CONTENT)

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

        if len(messages) < 1:
            return response_success("message isn't exist",{},status.HTTP_204_NO_CONTENT)

        my_unread_messages = Message.objects.filter(Q(sender=partner) & Q(receiver=user.id))
        for message in my_unread_messages:
            message.is_read = True
            message.save()

        serializer = MessageSerializer(messages, many=True)
        return response_success("success get data",serializer.data, status.HTTP_200_OK)

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
            return response_success("success sent message",serializer.data,status.HTTP_201_CREATED)

        return response_error("something went wrong",serializer.errors,status.HTTP_400_BAD_REQUEST)

class ChatRoomList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        list_chat_room = []
        chat_rooms = ChatRooms.objects.filter(Q(sender=request.user.id) | Q(receiver=request.user.id))
        for chat in chat_rooms:
            messages = Message.objects.filter(
                (Q(sender=chat.sender.id) & Q(receiver=chat.receiver.id)) |
                (Q(sender=chat.receiver.id) & Q(receiver=chat.sender.id))
            ).only('message').order_by('-timestamp').first()

            unread_chat = Message.objects.filter(
                (Q(sender=chat.sender.id) & Q(receiver=chat.receiver.id)) |
                (Q(sender=chat.receiver.id) & Q(receiver=chat.sender.id))
            ).filter(Q(is_read=False))
            count_unread_chat = len(unread_chat)

            chat_room_data = {
                'user_1' : chat.sender.username,
                'user_2' : chat.receiver.username,
                'last_message' : messages.message,
                'unread_message' : count_unread_chat
            }
            list_chat_room.append(chat_room_data)

        if len(list_chat_room) < 1:
            return response_success("no chat room available",list_chat_room,status.HTTP_204_NO_CONTENT)
        else:
            return response_success("success get list chat rooms",list_chat_room,status.HTTP_200_OK)