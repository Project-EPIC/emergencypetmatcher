# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_remove_petreport_revision_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petreport',
            name='microchip_id',
            field=models.CharField(default=b'', max_length=40, null=True),
        ),
    ]
