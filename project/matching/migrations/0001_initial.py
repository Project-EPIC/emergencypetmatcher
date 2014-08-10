# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PetMatch'
        db.create_table(u'matching_petmatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lost_pet', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='lost_pet_related', to=orm['reporting.PetReport'])),
            ('found_pet', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='found_pet_related', to=orm['reporting.PetReport'])),
            ('proposed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='proposed_by_related', to=orm['social.UserProfile'])),
            ('proposed_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_successful', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'matching', ['PetMatch'])

        # Adding M2M table for field up_votes on 'PetMatch'
        m2m_table_name = db.shorten_name(u'matching_petmatch_up_votes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('petmatch', models.ForeignKey(orm[u'matching.petmatch'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'social.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['petmatch_id', 'userprofile_id'])

        # Adding M2M table for field down_votes on 'PetMatch'
        m2m_table_name = db.shorten_name(u'matching_petmatch_down_votes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('petmatch', models.ForeignKey(orm[u'matching.petmatch'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'social.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['petmatch_id', 'userprofile_id'])


    def backwards(self, orm):
        # Deleting model 'PetMatch'
        db.delete_table(u'matching_petmatch')

        # Removing M2M table for field up_votes on 'PetMatch'
        db.delete_table(db.shorten_name(u'matching_petmatch_up_votes'))

        # Removing M2M table for field down_votes on 'PetMatch'
        db.delete_table(db.shorten_name(u'matching_petmatch_down_votes'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'matching.petmatch': {
            'Meta': {'object_name': 'PetMatch'},
            'down_votes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'down_votes_related'", 'null': 'True', 'to': u"orm['social.UserProfile']"}),
            'found_pet': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'found_pet_related'", 'to': u"orm['reporting.PetReport']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lost_pet': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'lost_pet_related'", 'to': u"orm['reporting.PetReport']"}),
            'proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposed_by_related'", 'to': u"orm['social.UserProfile']"}),
            'proposed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'up_votes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'up_votes_related'", 'null': 'True', 'to': u"orm['social.UserProfile']"})
        },
        u'reporting.petreport': {
            'Meta': {'object_name': 'PetReport'},
            'age': ('django.db.models.fields.CharField', [], {'default': "'Age unknown'", 'max_length': '10', 'null': 'True'}),
            'bookmarked_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'bookmarks_related'", 'null': 'True', 'to': u"orm['social.UserProfile']"}),
            'breed': ('django.db.models.fields.CharField', [], {'default': "'Breed unknown'", 'max_length': '30', 'null': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'Color(s) unknown'", 'max_length': '30', 'null': 'True'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'contact_link': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'date_lost_or_found': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True'}),
            'geo_location_lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5'}),
            'geo_location_long': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'microchip_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'pet_name': ('django.db.models.fields.CharField', [], {'default': "'Name unknown'", 'max_length': '15', 'null': 'True'}),
            'pet_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10'}),
            'proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'proposed_related'", 'to': u"orm['social.UserProfile']"}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'spayed_or_neutered': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '10', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5'}),
            'tag_info': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True'}),
            'thumb_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'workers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'workers_related'", 'null': 'True', 'to': u"orm['social.UserProfile']"})
        },
        u'social.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'null': 'True'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'followers'", 'null': 'True', 'to': u"orm['social.UserProfile']"}),
            'guardian_activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'guardian_consented': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guardian_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_path': ('django.db.models.fields.files.ImageField', [], {'default': "'userprofile/uploads/defaults/anonymous.gif'", 'max_length': '100', 'null': 'True'}),
            'is_minor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_logout': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'reputation': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'social_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thumb_path': ('django.db.models.fields.files.ImageField', [], {'default': "'userprofile/thumbnails/defaults/anonymous.gif'", 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['matching']