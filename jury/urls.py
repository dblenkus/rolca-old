from django.conf.urls import patterns, url

urlpatterns = patterns(  # pylint: disable=invalid-name
    'jury.views',

    url(r'^$', 'jury_app', name="jury_app"),
)
