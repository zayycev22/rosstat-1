from django.contrib.auth import authenticate
from django.db import IntegrityError
from drf_spectacular.utils import inline_serializer, extend_schema
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request as RestRequest

from auth_user.models import ExUser
from auth_user.serializers import AuthSerializer, RegisterSerializer


class Login(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(request=AuthSerializer, responses={
        200: inline_serializer(name="AuthSuccess", fields={
            "status": serializers.CharField(default="OK"),
            "token": serializers.CharField(),
        }),
        400: inline_serializer(name="AuthError", fields={
            "status": serializers.CharField(default="Error"),
            "detail": serializers.CharField(),
        })})
    def post(self, request: RestRequest):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user: ExUser = authenticate(email=serializer.validated_data["email"],
                                        password=serializer.validated_data["password"])
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"status": "OK", "token": token.key}, status=200)
            return Response({"status": "Error", "detail": "Неверный логин или пароль"}, status=400)
        return Response({"status": "Error", "detail": serializer.errors}, status=400)


class Register(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(request=RegisterSerializer, responses={
        201: inline_serializer(name="CreateSuccess", fields={
            "status": serializers.CharField(default="OK"),
            "token": serializers.CharField(),
        }),
        400: inline_serializer(name="CreateError", fields={
            "status": serializers.CharField(default="Error"),
            "detail": serializers.CharField(),
        })})
    def post(self, request: RestRequest):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            try:
                user.save()
            except IntegrityError:
                return Response({"status": "Error", "detail": "Что то пошло не так"}, status=400)
            else:
                return Response({"status": "OK", "detail": "Пользователь создан"}, status=201)
        return Response({"status": "Error", "detail": serializer.errors}, status=400)
