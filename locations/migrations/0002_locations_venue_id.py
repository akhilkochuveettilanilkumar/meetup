# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='venue_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
