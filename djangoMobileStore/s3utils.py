from storages.backends.s3boto3 import S3Boto3Storage

# StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')
# MediaRootS3BotoStorage  = lambda: S3Boto3Storage(location='media')

class MediaStorage(S3Boto3Storage):
    bucket_name = 'mobile-my-store'
    custom_domain = '{}.s3.amazonaws.com'.format(bucket_name)
    location = 'media'

class StaticStorage(S3Boto3Storage):
    bucket_name = 'mobile-my-store'
    custom_domain = '{}.s3.amazonaws.com'.format(bucket_name)
    location = 'static'