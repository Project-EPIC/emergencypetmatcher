# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PetMatch.has_failed'
        db.add_column(u'matching_petmatch', 'has_failed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PetMatch.has_failed'
        db.delete_column(u'matching_petmatch', 'has_failed')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
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
            'down_votes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'down_votes_related'", 'null': 'True', 'to': u"orm['socializing.UserProfile']"}),
            'found_pet': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'found_pet_related'", 'to': u"orm['reporting.PetReport']"}),
            'has_failed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lost_pet': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'lost_pet_related'", 'to': u"orm['reporting.PetReport']"}),
            'proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposed_by_related'", 'to': u"orm['socializing.UserProfile']"}),
            'proposed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'up_votes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'up_votes_related'", 'null': 'True', 'to': u"orm['socializing.UserProfile']"})
        },
        u'reporting.petreport': {
            'Meta': {'object_name': 'PetReport'},
            'age': ('django.db.models.fields.CharField', [], {'default': "'Age unknown'", 'max_length': '10', 'null': 'True'}),
            'bookmarked_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'bookmarks_related'", 'null': 'True', 'to': u"orm['socializing.UserProfile']"}),
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
            'proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'proposed_related'", 'to': u"orm['socializing.UserProfile']"}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'spayed_or_neutered': ('django.db.models.fields.CharField', [], {'default': "'Not Known'", 'max_length': '10', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5'}),
            'tag_info': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True'}),
            'thumb_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'workers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'workers_related'", 'null': 'True', 'to': u"orm['socializing.UserProfile']"})
        },
        u'socializing.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'null': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'followers'", 'null': 'True', 'to': u"orm['socializing.UserProfile']"}),
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