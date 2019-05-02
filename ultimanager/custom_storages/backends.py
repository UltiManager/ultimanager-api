"""Custom storage backends.
"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Storage class for media files.

    Prefixes all file paths with ``media/``.
    """

    bucket_name = settings.S3_BUCKET_MEDIA
    default_acl = "private"
    encryption = True
    location = "media"


class StaticStorage(S3Boto3Storage):
    """
    Storage class for static files.

    Prefixes all file paths with ``static/``.
    """

    bucket_name = settings.S3_BUCKET_STATIC
    default_acl = "public-read"
    location = "static"
    querystring_auth = False
