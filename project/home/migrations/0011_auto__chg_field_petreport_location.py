# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PetReport.location'
        db.alter_column('home_petreport', 'location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    def backwards(self, orm):

        # Changing field 'PetReport.location'
        db.alter_column('home_petreport', 'location', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'home.chat': {
            'Meta': {'object_name': 'Chat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pet_report': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': "orm['home.PetReport']", 'unique': 'True'})
        },
        'home.chatline': {
            'Meta': {'object_name': 'ChatLine'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['home.Chat']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10000', 'blank': 'True'}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['home.UserProfile']"})
        },
        'home.edituserprofile': {
            'Meta': {'object_name': 'EditUserProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'date_of_change': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': "orm['auth.User']", 'unique': 'True'})
        },
        'home.petmatch': {
            'Meta': {'object_name': 'PetMatch'},
            'closed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300'}),
            'down_votes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'down_votes_related'", 'null': 'True', 'to': "orm['home.UserProfile']"}),
            'found_pet': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'found_pet_related'", 'to': "orm['home.PetReport']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lost_pet': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'lost_pet_related'", 'to': "orm['home.PetReport']"}),
            'proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposed_by_related'", 'to': "orm['home.UserProfile']"}),
            'proposed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'up_votes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'up_votes_related'", 'null': 'True', 'to': "orm['home.UserProfile']"}),
            'verification_triggered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verification_votes': ('django.db.models.fields.CharField', [], {'default': "'00'", 'max_length': '2'})
        },
        'home.petreport': {
            'Meta': {'object_name': 'PetReport'},
            'age': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '10', 'null': 'True'}),
            'bookmarked_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'bookmarks_related'", 'null': 'True', 'to': "orm['home.UserProfile']"}),
            'breed': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '30', 'null': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '30', 'null': 'True'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'date_lost_or_found': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True'}),
            'geo_location_lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5'}),
            'geo_location_long': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'microchip_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'pet_name': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '15', 'null': 'True'}),
            'pet_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10'}),
            'proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'proposed_related'", 'to': "orm['home.UserProfile']"}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'spayed_or_neutered': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '10', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5'}),
            'tag_info': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'workers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'workers_related'", 'null': 'True', 'to': "orm['home.UserProfile']"})
        },
        'home.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'chats': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['home.Chat']", 'null': 'True', 'symmetrical': 'False'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'followers'", 'null': 'True', 'to': "orm['home.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_test': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_logout': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'reputation': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['home']