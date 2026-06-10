from .base import *

DEBUG = False

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Note: Media files are served through our custom RangeRequestMiddleware
# which provides proper byte-range support for seeking in audio/video

try:
    from .local import *
except ImportError:
    pass
