# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('institution', models.BooleanField(default=False)),
                ('institution_name', models.CharField(max_length=100, blank=True)),
                ('n_of_applicants', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('limit', models.IntegerField(null=True, blank=True)),
                ('location', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('instructor', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='workshop',
            field=models.ForeignKey(to='workshops.Workshop'),
        ),
    ]
