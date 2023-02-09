from django.urls import path
from .views import UserList,Message

urlpatterns = [
    path('users', UserList.as_view()),
    path('chat', Message.as_view())
]