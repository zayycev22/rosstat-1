from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers

from auth_user.models import ExUser


class AuthSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)


class RegisterSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=50)
    surname = serializers.CharField(max_length=50)

    def create(self, validated_data: dict) -> ExUser:
        password = validated_data.pop('password')
        user = ExUser(**validated_data)
        user.set_password(password)
        return user
