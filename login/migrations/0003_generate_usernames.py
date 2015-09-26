# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def generate_usernames(apps, schema_editor):
    Profile = apps.get_model("login", "Profile")
    for user in Profile.objects.all():
        username = user.email.split('@')[0].replace('.', '').replace('_', '')
        n = 0
        while Profile.objects.filter(username=username).exists():
            n += 1
            username = '{}_{}'.format(username.split('_')[0], n)

        user.username = username
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_add_username'),
    ]

    operations = [
        migrations.RunPython(generate_usernames),
    ]
