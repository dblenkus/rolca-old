from .settings import *  # NOQA

DEBUG = True
TEMPLATE_DEBUG = True
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

CACHES = {
    'default': {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:0",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
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
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'support@blenkus.com'
EMAIL_HOST_PASSWORD = 'I7zx5sye(A4si9'
