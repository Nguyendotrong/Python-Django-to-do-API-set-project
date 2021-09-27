from .models import Task
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import  User



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name', 'email', ]

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

    def create(self, validated_data):

        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'user', 'date_of_creation','status', 'date_of_modification', 'date_of_completion']


class TaskCreateSerializer(TaskSerializer):
    class Meta:
        model = TaskSerializer.Meta.model
        fields = TaskSerializer.Meta.fields + ['description']
        read_only_fields = ['id', 'date_of_creation', 'date_of_modification']


class TaskDetailSerializer(TaskCreateSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = TaskCreateSerializer.Meta.model
        fields  =  TaskCreateSerializer.Meta.fields
        read_only_fields = TaskCreateSerializer.Meta.read_only_fields


