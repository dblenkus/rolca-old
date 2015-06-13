from __future__ import absolute_import, division, print_function, unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ObjectDoesNotExist

from .models import Profile


class ProfileCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]  # pylint: disable=no-member
        try:
            Profile.objects.get(email=email)  # pylint: disable=no-member
            raise forms.ValidationError("A user with that email already exists.")
        except ObjectDoesNotExist:
            return email


class ProfileChangeForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(ProfileChangeForm, self).__init__(*args, **kwargs)
