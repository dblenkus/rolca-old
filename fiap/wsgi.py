import os

from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fiap.settings_rolcabox")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
application = Sentry(application)
