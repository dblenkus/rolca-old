# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uploader', '0002_auto_20151010_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 3, 751085, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 11, 31457, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 13, 787097, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participent',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 16, 104135, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 17, 801485, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 19, 469585, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salon',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 21, 139371, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salon',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 22, 737678, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salon',
            name='owner',
            field=models.ForeignKey(related_name='salons_owned', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theme',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 39, 454687, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theme',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 13, 41, 41, 260749, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salon',
            name='judges',
            field=models.ManyToManyField(related_name='salons_judged', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='theme',
            name='salon',
            field=models.ForeignKey(related_name='themes', to='uploader.Salon'),
        ),
    ]
