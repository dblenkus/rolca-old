import logging

from django.conf import settings


class PostgresLogHandler(logging.Handler):
    pass

def add_ravenJs_DSN(request):
    return {
        'RAVENJS_DSN': getattr(settings, "RAVENJS_DSN", ""),
    }

def add_analytics(request):
    return {
        'ANALYTICS': getattr(settings, "ANALYTICS", False),
    }
