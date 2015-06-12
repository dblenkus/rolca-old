from django.conf.urls import patterns, url
# from django.views.generic import TemplateView

urlpatterns = patterns(  # pylint: disable=invalid-name
    '',

    # url(r'^$', 'uploader.views.upload_app', name="upload_app"),
    # url(r'^potrditev$',
    #     TemplateView.as_view(template_name='uploader/upload_confirm.html'),
    #     name="upload_confirm"),

    # url(r'^$', 'uploader.views.upload', name="upload"),

    url(r'^$', 'results.views.select_results', name="select_results"),
    url(r'^(?P<salon_id>\d+)$', 'results.views.results', name="results"),

    url(r'^sole/$', 'results.views.select_school_results', name="select_school_results"),
    url(r'^sole/(?P<salon_id>\d+)$', 'results.views.school_results',
        name="school_results"),

    url(r'^foto/(?P<photo_id>\d+)$', 'results.views.photo_view', name="photo"),
)
