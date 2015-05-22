from django.conf.urls import patterns, url


urlpatterns = patterns(  # pylint: disable=invalid-name
    '',

    url(r'^potrditev/$', 'workshops.views.confirm', name="confirm"),
    url(r'^$', 'workshops.views.application', name="aplication"),
)
