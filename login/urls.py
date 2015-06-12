from __future__ import absolute_import, division, print_function, unicode_literals

import os

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# pylint: disable=line-too-long
urlpatterns = patterns(  # pylint: disable=invalid-name
    '',

    url(r'^prijava/$', 'login.views.login_view', name="login"),
    url(r'^registracija/$', 'login.views.signup_view', name="signup"),
    url(r'^registracija/potrditev$',
        TemplateView.as_view(template_name=os.path.join('login', 'signup_confirm.html')),
        name="signup_confirm"),
    url(r'^odjava/$', 'login.views.logout_view', name="logout"),

    # pasword reset
    url(r'^geslo/ponastavi/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'login/password_reset_form.html',
         'email_template_name': 'login/password_reset_email.html',
         'subject_template_name': 'login/password_reset_subject.txt'},
        name="password_reset"),
    url(r'^geslo/ponastavi/potrditev/$', 'django.contrib.auth.views.password_reset_done',
        {'template_name': 'login/password_reset_done.html', },
        name='password_reset_done'),
    url(r'^geslo/novo/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'login/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^geslo/novo/potrditev/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'login/password_reset_complete.html'},
        name='password_reset_complete'),


)
