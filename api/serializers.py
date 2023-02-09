from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','password']

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['sender','receiver','message']
