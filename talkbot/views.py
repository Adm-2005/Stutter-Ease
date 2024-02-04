from django.shortcuts import render
from rest_framework import generics
from .models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatMessageList(generics.ListCreateAPIView):
  queryset = ChatMessage.objects.all()
  serializer_class = ChatMessageSerializer
