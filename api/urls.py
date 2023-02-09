from django.urls import path
from .views import UserList,MessageHandler

urlpatterns = [
    path('users', UserList.as_view()),
    path('chat', MessageHandler.as_view())
]