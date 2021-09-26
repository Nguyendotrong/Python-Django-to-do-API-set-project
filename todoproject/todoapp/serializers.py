from .models import Task
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import  User


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'date_of_creation', 'date_of_modification']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        field = ['id', 'username', 'first_name','last_name' 'email', 'date_join']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

    def create(self, validated_data):

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        instance = user.save()
        return instance