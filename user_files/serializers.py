from rest_framework import serializers

from user_files.models import UserFile


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class FileListSerializer(serializers.ModelSerializer):
    filename: serializers.SerializerMethodField()

    class Meta:
        model = UserFile
        fields = ('filename',)


class FilenameSerializer(serializers.Serializer):
    filename: serializers.CharField()
