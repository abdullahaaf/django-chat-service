from django.urls import path
from .views import MessageHandler, ChatRoomList, RegisterApi

urlpatterns = [
    path('chat', MessageHandler.as_view()),
    path('chatroom', ChatRoomList.as_view()),
    path('register', RegisterApi.as_view())
]