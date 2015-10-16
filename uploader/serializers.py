from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from .models import File, Photo, Salon, Theme


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file',)


class PhotoSerializer(serializers.ModelSerializer):
    photo = FileSerializer()

    class Meta:
        model = Photo
        fields = ('id', 'photo', 'title')


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'title', 'n_photos')


class SalonSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True, read_only=True)

    class Meta:
        model = Salon
        fields = ('id', 'title', 'start_date', 'end_date', 'themes')
