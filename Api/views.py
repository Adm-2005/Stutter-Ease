from django.shortcuts import render
from rest_framework import generics
from .serializers import HomeSerializer


# Create your views here.
class HomeView(generics.ListAPIView):
    queryset = None
    serializer_class = HomeSerializer
