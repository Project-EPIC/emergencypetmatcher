# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0001_initial'),
        ('reporting', '0002_remove_petreport_revision_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetMatchCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_successful', models.BooleanField(default=False)),
                ('closed_date', models.DateTimeField(null=True)),
                ('verification_votes', models.CharField(default=b'00', max_length=2)),
                ('petmatch', models.OneToOneField(default=None, to='matching.PetMatch')),
            ],
        ),
        migrations.CreateModel(
            name='PetReunion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(default=None, max_length=200)),
                ('description', models.CharField(default=b'', max_length=500, null=True)),
                ('img_path', models.ImageField(null=True, upload_to=b'petreunion/uploads/')),
                ('thumb_path', models.ImageField(null=True, upload_to=b'petreunion/thumbnails/')),
                ('petreport', models.OneToOneField(default=None, to='reporting.PetReport')),
            ],
        ),
    ]
