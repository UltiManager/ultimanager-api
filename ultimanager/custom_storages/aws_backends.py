"""Custom storage backends.
"""
import os

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile


class PatchedS3StaticStorage(S3Boto3Storage):
    def _save_content(self, obj, content, parameters):
        """
        We create a clone of the content file as when this is passed to
        boto3 it wrongly closes the file upon upload where as the
        storage backend expects it to still be open.

        See Also:
            https://github.com/jschneier/django-storages/issues/382#issuecomment-377174808
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a
        # specified size
        content_autoclose = SpooledTemporaryFile()

        # Write our original content into our copy that will be closed
        # by boto3
        content_autoclose.write(content.read())

        # Upload the object which will auto close the content_autoclose
        # instance
        super(PatchedS3StaticStorage, self)._save_content(
            obj, content_autoclose, parameters
        )

        # Cleanup if this is fixed upstream our duplicate should always
        # close
        if not content_autoclose.closed:
            content_autoclose.close()


class CachedS3Storage(ManifestFilesMixin, PatchedS3StaticStorage):
    pass


class MediaStorage(S3Boto3Storage):
    """
    Storage class for media files.

    Prefixes all file paths with ``media/``.
    """

    bucket_name = settings.S3_BUCKET_MEDIA
    default_acl = "private"
    encryption = True
    location = "media"


class StaticStorage(CachedS3Storage):
    """
    Storage class for static files.

    Prefixes all file paths with ``static/``.
    """

    bucket_name = settings.S3_BUCKET_STATIC
    default_acl = "public-read"
    location = "static"
    querystring_auth = False
