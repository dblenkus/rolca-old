from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from .models import Profile, Institution


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'last_login')


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ('name',)
