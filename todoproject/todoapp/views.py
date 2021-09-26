from django.shortcuts import render
from .serializers import TaskSerializer, UserSerializer
# Create your views here.
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView

class User(viewsets.ViewSet, generics.ListAPIView,generics.CreateAPIView):
    serializer_class = UserSerializer
