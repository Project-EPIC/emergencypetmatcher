# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socializing', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pet_type', models.CharField(default=None, max_length=10, choices=[(b'Dog', b'Dog'), (b'Cat', b'Cat'), (b'Bird', b'Bird'), (b'Horse', b'Horse'), (b'Rabbit', b'Rabbit'), (b'Snake', b'Snake'), (b'Turtle', b'Turtle'), (b'Other', b'Other')])),
                ('status', models.CharField(default=None, max_length=5, choices=[(b'Lost', b'Lost'), (b'Found', b'Found')])),
                ('date_lost_or_found', models.DateField()),
                ('event_tag', models.CharField(max_length=100, null=True)),
                ('sex', models.CharField(max_length=6, null=True, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('size', models.CharField(max_length=30, null=True, choices=[(b'Extra Large', b'Extra Large'), (b'Large', b'Large'), (b'Medium', b'Medium'), (b'Small', b'Small')])),
                ('location', models.CharField(default=b'unknown', max_length=100, null=True)),
                ('geo_location_lat', models.FloatField(default=0.0, null=True)),
                ('geo_location_long', models.FloatField(default=0.0, null=True)),
                ('microchip_id', models.CharField(max_length=40, null=True)),
                ('tag_info', models.CharField(default=b'', max_length=500, null=True)),
                ('contact_name', models.CharField(default=b'None', max_length=50, null=True)),
                ('contact_number', models.CharField(default=b'None', max_length=30, null=True)),
                ('contact_email', models.CharField(default=b'None', max_length=50, null=True)),
                ('contact_link', models.CharField(default=b'None', max_length=300, null=True)),
                ('img_path', models.ImageField(null=True, upload_to=b'petreport/uploads/')),
                ('thumb_path', models.ImageField(null=True, upload_to=b'petreport/thumbnails/')),
                ('spayed_or_neutered', models.CharField(default=b'Not Known', max_length=10, null=True, choices=[(b'Not Known', b'Not Known'), (b'Spayed', b'Spayed'), (b'Neutered', b'Neutered'), (b'Neither', b'Neither')])),
                ('pet_name', models.CharField(default=b'unknown', max_length=30, null=True)),
                ('age', models.CharField(default=b'Age unknown', max_length=10, null=True, choices=[(b'Baby', b'Baby'), (b'Young', b'Young'), (b'Adult', b'Adult'), (b'Senior', b'Senior'), (b'Not Known', b'Not Known')])),
                ('color', models.CharField(default=b'Color(s) unknown', max_length=30, null=True)),
                ('breed', models.CharField(default=b'Breed unknown', max_length=90, null=True)),
                ('description', models.CharField(default=b'', max_length=1000, null=True)),
                ('closed', models.BooleanField(default=False)),
                ('revision_number', models.IntegerField(null=True)),
                ('bookmarked_by', models.ManyToManyField(related_name='bookmarks_related', to='socializing.UserProfile')),
                ('proposed_by', models.ForeignKey(related_name='proposed_related', default=None, to='socializing.UserProfile')),
                ('workers', models.ManyToManyField(related_name='workers_related', to='socializing.UserProfile')),
            ],
        ),
    ]
