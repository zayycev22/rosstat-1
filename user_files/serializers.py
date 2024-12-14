import datetime

from rest_framework import serializers

from global_settings.models import GlobalSettings
from user_files.models import UserFile


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class FileListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    created_exp = serializers.SerializerMethodField()

    def get_created_exp(self, obj: UserFile):
        settings = GlobalSettings.objects.get(id=1)
        return obj.created_exp + datetime.timedelta(seconds=settings.file_lifetime_seconds)

    def get_url(self, obj: UserFile) -> str:
        return obj.file.url

    class Meta:
        model = UserFile
        fields = ('filename', 'created_exp', 'url')


class FilenameSerializer(serializers.Serializer):
    filename: serializers.CharField()
