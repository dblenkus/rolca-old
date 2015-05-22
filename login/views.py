#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


from .models import UserProfile, Institution


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

        for key in required:
            if not values[key]:
                msg = "Prosim izpolnite vsa polja."
                if msg not in msgs:
                    msgs.append(msg)
                errors.append(key)

        try:
            user = UserProfile.objects.get(email=values['email'])
            msgs.append("Email naslov že obstaja.")
            errors.append('email')
        except ObjectDoesNotExist:
            pass

        if 'school' not in errors:
            try:
                Institution.objects.get(name__iexact=values['school'])
            except ObjectDoesNotExist:
                msgs.append('Prosim vnesite veljavno ime šole.')
                errors.append('school')

        if len(errors) == 0:
            password = UserProfile.objects.make_random_password()
            user = UserProfile.objects.create_user(password=password, **values)
            user.save()

            user = authenticate(email=values['email'], password=password)
            login(request, user)

            # user.email_user('Thanks for signing up!', 'Thanks')

            return redirect('upload_app')
            # return redirect('signup_confirm')

    response = {'msg': '<br>'.join(msgs), 'errors': errors}
    response.update({key: values[key] for key in fields})
    return render(request, os.path.join('login', 'signup.html'), response)


def login_view(request):
    msgs = []
    errors = []
    email = ''
    password = ''

    if request.method == 'POST':
        email = request.POST['email'] if 'email' in request.POST else ''
        password = request.POST['password'] if 'password' in request.POST else ''

        if not password:
            msgs.append("Prosim vpišite email.")
            errors.append('password')
        elif not email:
            msgs.append("Prosim vpišite geslo.")
            errors.append('email')
        else:
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(request.GET['next'] if 'next' in request.GET else 'index')
                else:
                    msgs.append("Vaš račun je bil onemogočen.")
            else:
                msgs.append("Email in geslo se ne ujemata.")
                errors.extend(['email', 'password'])

    response = {'msg': '<br>'.join(msgs), 'errors': errors, 'email': email,
                'password': password}
    return render(request, os.path.join('login', 'login.html'), response)


def logout_view(request):
    logout(request)
    return redirect('index')
