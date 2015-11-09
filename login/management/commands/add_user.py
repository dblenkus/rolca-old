"""
=================
Command: add_user
=================

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from django.core.management.base import BaseCommand, CommandError
from login.models import Profile


class Command(BaseCommand):

    """Create/update user with given email and password."""

    help = "Create/update user with given email and password."

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help="New user's email.")
        parser.add_argument('--password', type=str, help="New user's password.")
        parser.add_argument('--admin', action='store_true', help="Create admin user.")

    def handle(self, *args, **options):
        email = options['email'] or os.environ.get('DJANGO_USER_EMAIL', None)
        password = options['password'] or os.environ.get('DJANGO_USER_PASSWORD', None)
        admin = options['admin']

        if not email or not password:
            CommandError("Email, username and password are required")

        users_list = Profile.objects.filter(email=email)
        if users_list.exists():
            user = users_list.first()

            if (not user.check_password(password) or user.is_superuser != admin):
                user.set_password(password)
                user.is_superuser = admin
                user.save()
                return "User {} succesfully updated.".format(email)

            return "Nothing has changed."

        if admin:
            create_fn = Profile.objects.create_superuser
        else:
            create_fn = Profile.objects.create_user

        create_fn(email, password)

        return "User {} succesfully created".format(email)
