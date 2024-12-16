from storages.backends.s3boto3 import S3Boto3Storage


class YandexStorage(S3Boto3Storage):
    file_overwrite = False
    querystring_expire = 2592000
