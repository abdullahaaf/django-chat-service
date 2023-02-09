from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.http import Http404
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Message

from .serializers import UserSerializer, MessageSerializer

class UserList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MessageHandler(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

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

        serializer =MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        message_data = {
            'sender' : request.user.username,
            'receiver': request.data.get('receiver'),
            'message' : request.data.get('message')
        }

        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Success sent message",
                "data" : {
                    "sender" : request.user.username,
                    "receiver" : request.data.get('receiver'),
                    "text" : request.data.get("message")
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)