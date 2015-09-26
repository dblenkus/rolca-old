from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(  # pylint: disable=invalid-name
    '',

    url(r'^$', 'uploader.views.upload_app', name="upload_app"),
    url(r'^potrditev$',
        TemplateView.as_view(template_name='uploader/upload_confirm.html'),
        name="upload_confirm"),

    # url(r'^$', 'uploader.views.upload', name="upload"),

    url(r'^seznam$', 'uploader.views.list_select', name="list_select"),
    url(r'^seznam/(?P<salon_id>\d+)$', 'uploader.views.list_details',
        name="list_datails"),

    url(r'^razpisi$',
        TemplateView.as_view(template_name="uploader/notices.html"),
        name="notices"),
    url(r'^razpisi/os$',
        TemplateView.as_view(template_name="uploader/notice_os.html"),
        name="notice_os"),
    url(r'^razpisi/ss$',
        TemplateView.as_view(template_name="uploader/notice_ss.html"),
        name="notice_ss"),

)
