# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_remove_petreport_revision_number'),
        ('verifying', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='petreunion',
            name='matched_petreport',
            field=models.OneToOneField(related_name='matched_petreport', null=True, default=None, to='reporting.PetReport'),
        ),
    ]
