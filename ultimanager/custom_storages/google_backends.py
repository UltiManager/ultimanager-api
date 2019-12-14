from storages.backends.gcloud import GoogleCloudStorage


class MediaStorage(GoogleCloudStorage):
    """
    Storage class for media files.

    Prefixes all file paths with ``media/``.
    """

    location = "media"


class StaticStorage(GoogleCloudStorage):
    """
    Storage class for static files.

    Prefixes all the file paths for ``static/``.
    """

    default_acl = "publicRead"
    location = "static"
