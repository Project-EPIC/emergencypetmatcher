# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_remove_petreport_revision_number'),
        ('socializing', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proposed_date', models.DateTimeField(auto_now_add=True)),
                ('has_failed', models.BooleanField(default=False)),
                ('down_votes', models.ManyToManyField(related_name='down_votes_related', to='socializing.UserProfile')),
                ('found_pet', models.ForeignKey(related_name='found_pet_related', default=None, to='reporting.PetReport')),
                ('lost_pet', models.ForeignKey(related_name='lost_pet_related', default=None, to='reporting.PetReport')),
                ('proposed_by', models.ForeignKey(related_name='proposed_by_related', to='socializing.UserProfile')),
                ('up_votes', models.ManyToManyField(related_name='up_votes_related', to='socializing.UserProfile')),
            ],
        ),
    ]
