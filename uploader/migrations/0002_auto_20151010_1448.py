# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uploader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('mentor', models.CharField(max_length=30)),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='photo',
            name='user',
        ),
        migrations.AddField(
            model_name='photo',
            name='participent',
            field=models.ForeignKey(default=1, to='uploader.Participent'),
            preserve_default=False,
        ),
    ]
