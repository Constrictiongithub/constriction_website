from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage


class GoogleCloudStorageStatic(GoogleCloudStorage):
    location = settings.STATIC_ROOT.replace("/", "")


class GoogleCloudStorageMedia(GoogleCloudStorage):
    location = settings.MEDIA_ROOT.replace("/", "")
