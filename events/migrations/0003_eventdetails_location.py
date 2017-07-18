# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('events', '0002_auto_20170715_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdetails',
            name='location',
            field=models.ForeignKey(blank=True, to='locations.Locations', null=True),
        ),
    ]
