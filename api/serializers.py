import time

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Message, ChatRooms

class ChatRoomSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = ChatRooms
        fields = "__all__"
        fields = ['sender','receiver']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    
    class Meta:
        model = Message
        fields = ['sender','receiver','message','timestamp','is_read','previous']
