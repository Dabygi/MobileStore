from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

# StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')
# MediaRootS3BotoStorage  = lambda: S3Boto3Storage(location='media')

class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION

class MediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False