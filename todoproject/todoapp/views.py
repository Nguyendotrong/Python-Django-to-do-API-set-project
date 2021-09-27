from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import Task
from .paginator import BasePagination
from .serializers import TaskSerializer, UserSerializer, TaskDetailSerializer, TaskCreateSerializer
# Create your views here.
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from django.views.generic.edit import CreateView

class UserViewSet(viewsets.ViewSet, generics.ListAPIView,):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = BasePagination
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action=='sign_up':
            return [permissions.AllowAny(),]
        return [permissions.IsAuthenticated(),]

    @action(methods=['post'], detail=False, url_path='sign_up',
            url_name='sign_up')
    def sign_up(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

class TaskViewSet(viewsets.ViewSet, generics.UpdateAPIView,
                  generics.CreateAPIView, generics.ListAPIView,
                  generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Task.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskSerializer
        if self.action =='retrieve':
            return TaskDetailSerializer
        return TaskCreateSerializer

    def create(self, request, *args, **kwargs):
        if int(request.data.get('user')) == request.user.pk:
            raise PermissionDenied()
        return super().create(request,args,kwargs)

    @action(methods=['POST'],detail=True, url_path="assign-to-do", url_name='assign-to-do')
    def assign_to_do(self,request,*args,**kwargs):
        if request.data.get('user') is not None:
            user_id = int(request.data.get('user'))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task = self.get_object()
        if int(request.data.get('user')) == request.user.pk or task.status== 'COMPLETE':
            raise PermissionDenied()

        task = self.get_object()
        # task.user = user_id
        # task.save()
        serializer = TaskCreateSerializer(task, data={'user':user_id}, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        if request.data.get('user') is not None:
            user_id = int(request.data.get('user'))
            if user_id == request.user.id:
                raise PermissionDenied()

        if task.status == 'COMPLETE' :
            raise PermissionDenied()
        return super().update(request,partial=True)




