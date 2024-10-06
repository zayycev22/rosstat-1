from django.urls import path

from user_files.views import UploadFile, UserFileList, DownloadFile, DeleteFile

urlpatterns = [
    path("upload_file", UploadFile.as_view(), name="upload_file"),
    path("", UserFileList.as_view(), name="filelist"),
    path("download_file/<str:filename>", DownloadFile.as_view(), name="download_file"),
    path("delete_file/<str:filename>", DeleteFile.as_view(), name="download_file")
]
