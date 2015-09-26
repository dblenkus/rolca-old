from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.crypto import get_random_string


from uploader.models import Salon


def get_tomorrow():
    return timezone.now() + timedelta(days=1)


def generate_token():
    return get_random_string(length=32)


class Confirmation(models.Model):

    """Tokens for confirming email adresses."""

    #: user's profile
    profile = models.ForeignKey('Profile')

    #: confirmation token
    token = models.CharField(max_length=32, default=generate_token)

    #: expiration date
    expiration = models.DateTimeField(default=get_tomorrow)

    def __unicode__(self):
        # pylint: disable=no-member
        return "uid:{} token:{}".format(self.profile.pk, self.token)


class ProfileManager(UserManager):

    """Custom user manager for `Profile` model."""

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """Creates and saves a User with the given email and password."""
        user = self.model(email=email, is_staff=is_staff,  # pylint: disable=no-member
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # pylint: disable=no-member
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class Mentor(models.Model):
    """Model for linking Users with their mentors.

    Link can be represented as mentor's name in `name` field or as
    reference to other `Profile` instance in `reference` field.

    """
    #: mentors name
    name = models.CharField(max_length=100, blank=True)

    #: reference to mentor's profile
    reference = models.ForeignKey('Profile', blank=True, null=True,
                                  limit_choices_to={'is_mentor': True},
                                  related_name='mentor_profile')

    def __unicode__(self):
        return self.name if self.name else unicode(self.reference)


class Profile(AbstractBaseUser, PermissionsMixin):
    """Custom user model

        Fields inherited from AbstracBasetUser:
        - password
        - last_login

        Fields inherited from PermissionsMixin:
        - groups
        - user_permissions
        - is_superuser

    """

    #: user's email
    email = models.EmailField('email address')

    #: user's first name
    first_name = models.CharField(max_length=30)

    #: user's last name
    last_name = models.CharField(max_length=30)

    #: username
    username = models.CharField(max_length=30, unique=True)

    #: user's address
    address = models.CharField(max_length=100)

    #: user's post number
    post = models.CharField(max_length=100)

    #: user's school
    school = models.CharField(max_length=100)

    #: indicate if user is mentor
    is_mentor = models.BooleanField(default=False)

    #: user's mentor
    mentor = models.ForeignKey(Mentor, blank=True, null=True)

    #: indicate if user is activated
    is_active = models.BooleanField('active', default=False)

    #: indicate if user is staff
    is_staff = models.BooleanField('staff status', default=False)

    #: date joined
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = ProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'

    def get_full_name(self):
        """Return user's full name."""
        full_name = u'{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return user's last name and first character of first name."""
        initial = self.first_name[0] if len(self.first_name) > 0 else ''
        return u'{} {}.'.format(self.last_name, initial)

    def email_user(self, subject, message, from_email=None):
        """Send email to user."""
        email = EmailMessage(subject, message, from_email, [self.email])
        email.send(fail_silently=True)

    def get_token(self):
        return Confirmation.objects.create(profile=self).token

    def is_judge(self):
        """Check if user is judge in any saloon."""
        salons = Salon.objects.filter(judges=self)
        return len(salons) > 0

    def __unicode__(self):
        return self.get_full_name()


class Institution(models.Model):
    name = models.CharField(max_length=100, unique=True)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return u'{}'.format(self.name)
