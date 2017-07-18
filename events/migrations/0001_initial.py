# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('link', models.URLField(max_length=1000, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('duration', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('fee', models.FloatField(null=True, blank=True)),
                ('currency', models.CharField(max_length=10, null=True, blank=True)),
                ('status', models.CharField(max_length=25, null=True, blank=True)),
                ('group', models.CharField(max_length=250, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
