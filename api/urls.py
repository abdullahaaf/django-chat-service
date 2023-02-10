from django.urls import path
from .views import MessageHandler, ChatRoomList

urlpatterns = [
    path('chat', MessageHandler.as_view()),
    path('chatroom', ChatRoomList.as_view())
]