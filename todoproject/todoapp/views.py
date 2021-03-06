from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import  action
from django.db import IntegrityError

from .models import Task
from .paginator import BasePagination
from .serializers import TaskSerializer, UserSerializer, TaskDetailSerializer, TaskCreateSerializer



class UserViewSet(viewsets.ViewSet, generics.ListAPIView,):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = BasePagination
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action=='sign_up':
            return [permissions.AllowAny(),]
        return [permissions.IsAuthenticated(),]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     instance = serializer.save()
    #     instance = User.objects.get(username=request.data.get('username'))
    #     instance.set_password(request.data.get('password'))
    #     instance.save()
    #     headers = self.get_success_headers(instance)
    #
    #     return Response(UserSerializer(instance).data, status=status.HTTP_201_CREATED,headers=headers )

    @action(methods=['POST'], detail=False, url_path='sign-up',
            url_name='sign-up')
    def sign_up(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = User.objects.get(username=request.data.get('username'))
        instance.set_password(request.data.get('password'))
        instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

        try:
            if int(request.data.get('user')) == request.user.pk:
                raise PermissionDenied()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # try catch ????? b???t l???i n???u nh???p ng??y ho??n th??nh task..
            # ..nh??? h??n ng??y t???o task s??? xu???t error c???a contrain b??n model

        except IntegrityError:
            raise ValidationError(detail='completion date must not be less than creation date')
        except ValueError:
            raise  ValidationError(detail="user field must be interger")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


        def perform_create(self, serializer):
            serializer.save()

        def get_success_headers(self, data):
            try:
                return {'Location': str(data[api_settings.URL_FIELD_NAME])}
            except (TypeError, KeyError):
                return {}

    @action(methods=['POST'],detail=True, url_path="assign-to-do", url_name='assign-to-do')
    def assign_to_do(self,request,*args,**kwargs):
        if request.data.get('user') is not None:
            user_id = int(request.data.get('user'))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task = self.get_object()
        if int(request.data.get('user')) == request.user.pk or task.status== 1:
            raise PermissionDenied()

        task = self.get_object()
        serializer = TaskCreateSerializer(task, data={'user':user_id}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        #ki???m tra c?? c???p nh???t bi???n user hay kh??ng..
        # ..n???u c?? th?? ki???m tra ko cho ph??n task cho user ??ang ????ng nh???p
        if request.data.get('user') is not None:
            try:
                user_id = int(request.data.get('user'))
                if user_id == request.user.id:
                    raise PermissionDenied()
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if task.status == 1 :
            raise PermissionDenied()

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        try:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except IntegrityError:
            raise ValidationError(detail='completion date must not be less than creation date')

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)




