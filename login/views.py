# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import exceptions, filters, permissions, viewsets

from .models import Confirmation, Institution, Mentor, Profile
from .permissions import ProfilePermissions
from .serializers import InstitutionSerializer, ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermissions,)

    def get_queryset(self):
        user = self.request.user

        # `mentor_profile__reference must be `Profile` instance, not
        # `AnonymousUser`
        if not user.is_authenticated():
            return Profile.objects.none()

        if user.is_staff or user.is_superuser:
            return Profile.objects.all()

        return Profile.objects.filter(Q(pk=user.pk) | Q(mentor__reference=user))

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise exceptions.NotFound
        if not request.user.is_mentor:
            raise exceptions.PermissionDenied

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
    user = request.user
    msgs = []
    errors = []
    fields = ['first_name', 'last_name', 'email', 'address', 'post', 'school', 'mentor']
    required = ['first_name', 'last_name', 'email', 'address', 'post', 'school']
    values = {key: '' for key in fields}

    if request.method == 'POST':
        values = {key: request.POST[key] if key in request.POST
                       else '' for key in fields}

        values['is_mentor'] = ('is_mentor' in request.POST and
                               request.POST['is_mentor'] == 'on')

        for key in required:
            if not values[key]:
                msg = "Prosim izpolnite vsa polja."
                if msg not in msgs:
                    msgs.append(msg)
                errors.append(key)

        values['email'] = values['email'].strip()

        profile_qs = Profile.objects.filter(
            first_name=values['first_name'], last_name=values['last_name'],
            email=values['email']
        )

        if profile_qs.exists():
            if profile_qs.first().photo_set.exists():
                msgs.append("Uporabnik že obstaja.")
                errors.append('email')
            else:
                profile_qs.delete()

        if ('school' not in errors and
                not Institution.objects.filter(name__iexact=values['school']).exists()):
            msgs.append('Prosim vnesite veljavno ime šole.')
            errors.append('school')

        if len(errors) == 0:
            if values['mentor']:
                values['mentor'] = Mentor.objects.get_or_create(name=values['mentor'])[0]
            else:
                del values['mentor']

            username = values['email'].split('@')[0].replace('.', '').replace('_', '')
            n = 0
            while Profile.objects.filter(username=username).exists():
                n += 1
                username = '{}_{}'.format(username.split('_')[0], n)

            password = Profile.objects.make_random_password()
            user = Profile.objects.create_user(username=username, password=password,
                                               **values)
            user.is_active = True
            user.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            # _send_confirmation(request, user, password)

            return redirect('upload_app')

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
    username = ''
    password = ''

    if request.method == 'POST':
        username = request.POST['username'] if 'username' in request.POST else ''
        password = request.POST['password'] if 'password' in request.POST else ''

        if not username:
            msgs.append("Prosim vpišite uporabniško ime.")
            errors.append('username')
        elif not password:
            msgs.append("Prosim vpišite geslo.")
            errors.append('password')
        else:
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(
                        request.GET['next'] if 'next' in request.GET else 'upload_app')
                else:
                    msgs.append("Vaš račun je bil onemogočen.")
            else:
                msgs.append("Uporabniško ime in geslo se ne ujemata.")
                errors.extend(['username', 'password'])

    response = {'msg': '<br>'.join(msgs), 'errors': errors, 'username': username,
                'password': password}
    return render(request, os.path.join('login', 'login.html'), response)


def logout_view(request):
    logout(request)
    return redirect('index')
