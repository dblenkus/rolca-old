# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import exceptions, filters, permissions, viewsets

from .models import Confirmation, Institution, Profile
from .permissions import ProfilePermissions
from .serializers import InstitutionSerializer, ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermissions,)

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated():
            return Profile.objects.none()

        if user.is_staff or user.is_superuser:
            return Profile.objects.all()

        return Profile.objects.filter(pk=user.pk)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise exceptions.NotFound

        return super(ProfileViewSet, self).create(request, *args, **kwargs)


class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Institution.objects.filter(enabled=True)
    permission_classes = (permissions.AllowAny,)
    serializer_class = InstitutionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


def _send_confirmation(request, user, password):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    context = Context({
        'domain': domain,
        'email': user.email,
        'password': password,
        'protocol': 'https' if request.is_secure() else 'http',
        'site_name': site_name,
        'token': user.get_token(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    })
    email_body = get_template(os.path.join('login', 'confirmation_email.html'))
    user.email_user('Registracija', email_body.render(context))


def signup_view(request):
    msgs = []
    errors = []
    fields = ['first_name', 'last_name', 'email', 'address', 'post', 'school']
    values = {key: '' for key in fields}

    if request.method == 'POST':
        values = {key: request.POST[key] if key in request.POST
                       else '' for key in fields}

        for key in fields:
            if not values[key]:
                msg = "Prosim izpolnite vsa polja."
                if msg not in msgs:
                    msgs.append(msg)
                errors.append(key)

        if Profile.objects.filter(email=values['email']).exists():
            msgs.append("Email naslov že obstaja.")
            errors.append('email')

        if ('school' not in errors and
                not Institution.objects.filter(name__iexact=values['school']).exists()):
            msgs.append('Prosim vnesite veljavno ime šole.')
            errors.append('school')

        if len(errors) == 0:
            password = Profile.objects.make_random_password()
            user = Profile.objects.create_user(password=password, **values)

            _send_confirmation(request, user, password)

            return redirect('signup_confirm')

    response = {'msg': '<br>'.join(msgs), 'errors': errors}
    response.update({key: values[key] for key in fields})
    return render(request, os.path.join('login', 'signup.html'), response)


def activate(request, uidb64, token):  # pylint: disable=unused-argument
    uid = force_text(urlsafe_base64_decode(uidb64))

    if not Confirmation.objects.filter(profile=uid, token=token).exists():
        return redirect('activation_bad')

    Profile.objects.filter(pk=uid).update(is_active=True)
    Confirmation.objects.filter(profile=uid).delete()

    return redirect('activation_ok')


def login_view(request):
    msgs = []
    errors = []
    email = ''
    password = ''

    if request.method == 'POST':
        email = request.POST.get('email', email)
        password = request.POST.get('password', password)

        if not email:
            msgs.append("Prosim vpišite email naslov.")
            errors.append('email')
        elif not password:
            msgs.append("Prosim vpišite geslo.")
            errors.append('password')
        else:
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(request.GET.get('next', 'upload_app'))
                else:
                    msgs.append("Vaš račun je bil onemogočen.")
            else:
                msgs.append("Email naslov in geslo se ne ujemata.")
                errors.extend(['email', 'password'])

    response = {
        'msg': '<br>'.join(msgs),
        'errors': errors,
        'email': email,
        'password': password}
    return render(request, os.path.join('login', 'login.html'), response)


def logout_view(request):
    logout(request)
    return redirect('index')
