from django.urls import path
from .views import ChatMessageList

urlpatterns = [
  path('messages/', ChatMessageList.as_view(), name="chat-message-list"),
]