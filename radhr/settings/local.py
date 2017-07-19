from .base import *

################################################################################
## Static Files: Setup File Storage.                                          ##
################################################################################
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")
PROTECTED_ROOT = os.path.join(BASE_DIR, "static_cdn", "protected")
################################################################################
## Media Files: Setup File Storage.                                          ##
################################################################################
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media_cdn")
# DATABASE - LOCAL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}