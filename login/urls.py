from __future__ import absolute_import, division, print_function, unicode_literals

import os

from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as dj_views

from . import views

# pylint: disable=line-too-long
urlpatterns = [  # pylint: disable=invalid-name
    # login
    url(r'^prijava/$', views.login_view, name='login'),

    # logout
    url(r'^odjava/$', views.logout_view, name='logout'),

    # signup
    url(r'^registracija/$', views.signup_view, name='signup'),
    url(r'^registracija/potrditev/$',
        TemplateView.as_view(template_name=os.path.join('login', 'signup_confirm.html')),
        name='signup_confirm'),

    # activation
    url(r'^aktivacija/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{32})/$',
        views.activate, name='signup_activation'),
    url(r'^aktivacija/uspela/$',
        TemplateView.as_view(template_name=os.path.join('login', 'activation_ok.html')),
        name='activation_ok'),
    url(r'^aktivacija/neuspela/$',
        TemplateView.as_view(template_name=os.path.join('login', 'activation_bad.html')),
        name='activation_bad'),

    # pasword reset
    url(r'^geslo/ponastavi/$', dj_views.password_reset,
        {'template_name': 'login/password_reset_form.html',
         'email_template_name': 'login/password_reset_email.html',
         'subject_template_name': 'login/password_reset_subject.txt'},
        name="password_reset"),
    url(r'^geslo/ponastavi/potrditev/$', dj_views.password_reset_done,
        {'template_name': 'login/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^geslo/novo/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa
        dj_views.password_reset_confirm,
        {'template_name': 'login/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^geslo/novo/potrditev/$', dj_views.password_reset_complete,
        {'template_name': 'login/password_reset_complete.html'},
        name='password_reset_complete'),
]
