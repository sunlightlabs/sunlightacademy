from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class BetterS3BotoStorage(S3BotoStorage):

    def url(self, name):
        if settings.DEBUG:
            return settings.STATIC_URL + name
        return super(BetterS3BotoStorage, self).url(name)
