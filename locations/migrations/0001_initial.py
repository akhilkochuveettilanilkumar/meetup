# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=1000, null=True, blank=True)),
                ('country_code', models.CharField(max_length=50, null=True, blank=True)),
                ('localized_country_name', models.CharField(max_length=100, null=True, blank=True)),
                ('state', models.CharField(max_length=1000, null=True, blank=True)),
                ('latitude', models.FloatField(default=None)),
                ('longitude', models.FloatField(default=None)),
                ('zip_code', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
