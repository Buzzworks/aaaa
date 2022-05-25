from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin

class MediaStore(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """
    Google file storage class which gives a media file path from       MEDIA_URL not google generated one.
    """
    bucket_name = setting('GS_BUCKET_NAME')
    def url(self, name):
        """
        Gives correct MEDIA_URL and not google generated url.
        """
        return urljoin(settings.MEDIA_URL, name)