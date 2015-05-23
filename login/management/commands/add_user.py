"""
=================
Command: add_user
=================

"""
import os

from django.core.management.base import BaseCommand, CommandError
from login.models import UserProfile


class Command(BaseCommand):

    """Create/update user with given email and password."""

    help = "Create/update user with given email and password."

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help="New user's email.")
        parser.add_argument(
            '--password',
            type=str,
            help="New user's password.")
        parser.add_argument(
            '--admin',
            action='store_true',
            help="Create admin user.")

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        admin = options['admin']

        if not email and 'DJANGO_USER_EMAIL' in os.environ:
            email = os.environ['DJANGO_USER_EMAIL']
        if not password and 'DJANGO_USER_PASSWORD' in os.environ:
            password = os.environ['DJANGO_USER_PASSWORD']

        if not email or not password:
            CommandError("Email and password are required")

        users_list = UserProfile.objects.filter(email=email)
        if len(users_list) == 1:
            user = users_list[0]

            if not user.check_password(password) or user.is_superuser != admin:
                user.set_password(password)
                user.is_superuser = admin
                user.save()
                return "User {} succesfully updated.".format(email)

            return "Nothing has changed."

        if admin:
            create_fn = UserProfile.objects.create_superuser
        else:
            create_fn = UserProfile.objects.create_user

        create_fn(email=email, password=password)

        return "User {} succesfully created".format(email)
