"""Custom storage backends.
"""
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from storages.backends.s3boto3 import S3Boto3Storage


class PatchedS3StaticStorage(S3Boto3Storage):
    def _save(self, name, content):
        if (
            hasattr(content, "seek")
            and hasattr(content, "seekable")
            and content.seekable()
        ):
            content.seek(0)
        return super()._save(name, content)


class CachedS3Storage(ManifestFilesMixin, PatchedS3StaticStorage):
    pass


class MediaStorage(CachedS3Storage):
    """
    Storage class for media files.

    Prefixes all file paths with ``media/``.
    """

    bucket_name = settings.S3_BUCKET_MEDIA
    default_acl = "private"
    encryption = True
    location = "media"


class StaticStorage(ManifestFilesMixin, S3Boto3Storage):
    """
    Storage class for static files.

    Prefixes all file paths with ``static/``.
    """

    bucket_name = settings.S3_BUCKET_STATIC
    default_acl = "public-read"
    location = "static"
    querystring_auth = False
