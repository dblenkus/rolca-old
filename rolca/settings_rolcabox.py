from .settings import *  # NOQA

DEBUG = True
COMPRESS_ENABLED = False
HTML_MINIFY = False

TEST_SELENIUM = False

ALLOWED_HOSTS = ['127.0.0.1', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rolcabox',
        'USER': 'rolcabox',
        'PASSWORD': 'b4bxje',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}

BROKER_URL = "amqp://rolca:b4bxje@localhost:5672/rolca_broker"

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

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..', 'static'))
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..', 'media'))
MEDIA_URL = '/media/'

# email settings
CELERY_EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/webapps/rolcabox/emails'
