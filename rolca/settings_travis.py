from .settings import *  # NOQA

DEBUG = False
COMPRESS_ENABLED = True
HTML_MINIFY = True

TEST_SELENIUM = False

ALLOWED_HOSTS = ['*', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rolca',
        'USER': 'postgres',
    }
}

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'media'))
MEDIA_URL = '/media/'

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'emails'
