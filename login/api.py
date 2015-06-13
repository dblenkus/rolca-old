from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers, viewsets, filters

from .models import Profile, Institution


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'last_login')


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()  # pylint: disable=no-member
    serializer_class = ProfileSerializer


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ('name',)


class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Institution.objects.filter(enabled=True)
    serializer_class = InstitutionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
