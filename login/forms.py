from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ObjectDoesNotExist

from .models import UserProfile


class UserProfileCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(UserProfileCreationForm, self).__init__(*args, **kwargs)
        del self.fields['username']  # pylint: disable=no-member

    def clean_email(self):
        email = self.cleaned_data["email"]  # pylint: disable=no-member
        try:
            UserProfile.objects.get(email=email)  # pylint: disable=no-member
            raise forms.ValidationError("A user with that email already exists.")
        except ObjectDoesNotExist:
            return email


class UserProfileChangeForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = UserProfile

    def __init__(self, *args, **kwargs):
        super(UserProfileChangeForm, self).__init__(*args, **kwargs)
        del self.fields['username']  # pylint: disable=no-member
