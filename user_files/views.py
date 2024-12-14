import datetime
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import StreamingHttpResponse
from drf_spectacular.utils import inline_serializer, extend_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request as RestRequest
from rest_framework.parsers import MultiPartParser
from django.conf import settings

from global_settings.models import GlobalSettings, FileExtension
from user_files.consts import UserFileConsts
from user_files.models import UserFile
from rest_framework.generics import ListAPIView

from user_files.serializers import FileUploadSerializer, FileListSerializer, FilenameSerializer


class UploadFile(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=FileUploadSerializer, responses={
        200: inline_serializer(name="UploadSuccess", fields={
            "status": serializers.CharField(default="OK"),
            "detail": serializers.CharField(),
        }),
        400: inline_serializer(name="UploadError", fields={
            "status": serializers.CharField(default="Error"),
            "detail": serializers.CharField(),
        })})
    def post(self, request: RestRequest):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file: InMemoryUploadedFile = request.FILES['file']
            file_size = GlobalSettings.objects.get(id=1)
            file_size_bytes = file_size.file_size * 1024 * 1024
            if uploaded_file.size > file_size_bytes:
                return Response({"status": "Error", "detail": "Файл превысил объем"}, status=406)
            extension = uploaded_file.name.split('.')[-1]
            extensions = FileExtension.objects.filter(extension=extension)
            if not extensions.exists():
                return Response({"status": "Error", "detail": "Неподдерживаемый формат файла"}, status=406)
            try:
                user_file = UserFile.objects.get(filename=uploaded_file.name, user=request.user)
                user_file.file.delete()
                user_file.file = uploaded_file
                user_file.created_exp = datetime.datetime.now()
                user_file.save()
            except UserFile.DoesNotExist:
                exp = datetime.datetime.now() + datetime.timedelta(
                    seconds=settings.FILE_LIFETIME_SECONDS)
                user_file = UserFile(filename=uploaded_file.name, file=uploaded_file, user=request.user,
                                     created_exp=exp)
                user_file.save()
            return Response({"status": "OK", "detail": "Файл загружен"}, status=200)
        return Response({"status": "Error", "detail": serializer.errors}, status=400)


class UserFileList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FileListSerializer

    def get_queryset(self):
        queryset = UserFile.objects.filter(user=self.request.user)
        return queryset


class DownloadFile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: RestRequest, filename: str):
        try:
            file_obj = UserFile.objects.get(user=self.request.user, filename=filename)
        except UserFile.DoesNotExist:
            return Response({"status": "Error", "detail": "Файл не найден"}, status=400)
        else:
            mime_type = UserFileConsts.MIME_TYPES[file_obj.filename.split('.')[-1]]
            data = file_obj.file.read()
            data_io = BytesIO(data)
            response = StreamingHttpResponse(iter([data_io.getvalue()]), status=200, content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename={file_obj.filename}'
            response['filename'] = file_obj.filename
            response['Cache-Control'] = 'no-cache'
            response["Access-Control-Expose-Headers"] = "Content-Disposition"
            return response


class DeleteFile(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=FilenameSerializer, responses={
        200: inline_serializer(name="DeleteSuccess", fields={
            "status": serializers.CharField(default="OK"),
            "detail": serializers.CharField(),
        }),
        400: inline_serializer(name="DeleteError", fields={
            "status": serializers.CharField(default="Error"),
            "detail": serializers.CharField(),
        })})
    def delete(self, request: RestRequest, filename: str):
        try:
            file = UserFile.objects.get(filename=filename, user=request.user)
        except UserFile.DoesNotExist:
            return Response({"status": "Error", "detail": "Файл не найден"}, status=400)
        else:
            file.delete()
        return Response({"status": "Error", "detail": "Файл удален"}, status=200)
