from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns(  # pylint: disable=invalid-name
    '',

    url(r'^$', 'frontend.views.index', name="upload_app"),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',

        url(r'^400$', TemplateView.as_view(template_name="400.html"), name='400'),
        url(r'^403$', TemplateView.as_view(template_name="403.html"), name='403'),
        url(r'^404$', TemplateView.as_view(template_name="404.html"), name='404'),
        url(r'^500$', TemplateView.as_view(template_name="500.html"), name='500'),
    )
