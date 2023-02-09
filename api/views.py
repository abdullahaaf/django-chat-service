from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404

from .models import Message
from django.contrib.auth.models import User

from .serializers import UserSerializer, MessageSerializer

class UserList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Message(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        sender = self.get_user(request.user.username)
        receiver = self.get_user(request.data.get('receiver'))
        message_data = {
            'sender' : sender.id,
            'receiver': receiver.id,
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