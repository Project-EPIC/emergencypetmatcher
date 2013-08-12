# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('home_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(default=None, to=orm['auth.User'], unique=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('last_logout', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('is_test', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reputation', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
        ))
        db.send_create_signal('home', ['UserProfile'])

        # Adding M2M table for field following on 'UserProfile'
        db.create_table('home_userprofile_following', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm['home.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm['home.userprofile'], null=False))
        ))
        db.create_unique('home_userprofile_following', ['from_userprofile_id', 'to_userprofile_id'])

        # Adding M2M table for field chats on 'UserProfile'
        db.create_table('home_userprofile_chats', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['home.userprofile'], null=False)),
            ('chat', models.ForeignKey(orm['home.chat'], null=False))
        ))
        db.create_unique('home_userprofile_chats', ['userprofile_id', 'chat_id'])

        # Adding model 'PetReport'
        db.create_table('home_petreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pet_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=10)),
            ('status', self.gf('django.db.models.fields.CharField')(default=None, max_length=5)),
            ('date_lost_or_found', self.gf('django.db.models.fields.DateField')()),
            ('proposed_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='proposed_related', to=orm['home.UserProfile'])),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=6, null=True)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('geo_location_lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5)),
            ('geo_location_long', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5)),
            ('microchip_id', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('tag_info', self.gf('django.db.models.fields.CharField')(default='', max_length=500, null=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('contact_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('img_path', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('thumb_path', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('spayed_or_neutered', self.gf('django.db.models.fields.CharField')(default='Not Known', max_length=10, null=True)),
            ('pet_name', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=15, null=True)),
            ('age', self.gf('django.db.models.fields.CharField')(default='Not Known', max_length=10, null=True)),
            ('color', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=30, null=True)),
            ('breed', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=30, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default=' ', max_length=1000, null=True)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('revision_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('home', ['PetReport'])

        # Adding M2M table for field workers on 'PetReport'
        db.create_table('home_petreport_workers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('petreport', models.ForeignKey(orm['home.petreport'], null=False)),
            ('userprofile', models.ForeignKey(orm['home.userprofile'], null=False))
        ))
        db.create_unique('home_petreport_workers', ['petreport_id', 'userprofile_id'])

        # Adding M2M table for field bookmarked_by on 'PetReport'
        db.create_table('home_petreport_bookmarked_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('petreport', models.ForeignKey(orm['home.petreport'], null=False)),
            ('userprofile', models.ForeignKey(orm['home.userprofile'], null=False))
        ))
        db.create_unique('home_petreport_bookmarked_by', ['petreport_id', 'userprofile_id'])

        # Adding model 'PetMatch'
        db.create_table('home_petmatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lost_pet', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='lost_pet_related', to=orm['home.PetReport'])),
            ('found_pet', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='found_pet_related', to=orm['home.PetReport'])),
            ('proposed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='proposed_by_related', to=orm['home.UserProfile'])),
            ('proposed_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=300, null=True)),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_successful', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verification_triggered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('closed_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('verification_votes', self.gf('django.db.models.fields.CharField')(default='00', max_length=2)),
        ))
        db.send_create_signal('home', ['PetMatch'])

        # Adding M2M table for field up_votes on 'PetMatch'
        db.create_table('home_petmatch_up_votes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('petmatch', models.ForeignKey(orm['home.petmatch'], null=False)),
            ('userprofile', models.ForeignKey(orm['home.userprofile'], null=False))
        ))
        db.create_unique('home_petmatch_up_votes', ['petmatch_id', 'userprofile_id'])

        # Adding M2M table for field down_votes on 'PetMatch'
        db.create_table('home_petmatch_down_votes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('petmatch', models.ForeignKey(orm['home.petmatch'], null=False)),
            ('userprofile', models.ForeignKey(orm['home.userprofile'], null=False))
        ))
        db.create_unique('home_petmatch_down_votes', ['petmatch_id', 'userprofile_id'])

        # Adding model 'Chat'
        db.create_table('home_chat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pet_report', self.gf('django.db.models.fields.related.OneToOneField')(default=None, to=orm['home.PetReport'], unique=True)),
        ))
        db.send_create_signal('home', ['Chat'])

        # Adding model 'ChatLine'
        db.create_table('home_chatline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chat', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['home.Chat'])),
            ('userprofile', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['home.UserProfile'])),
            ('text', self.gf('django.db.models.fields.CharField')(default=None, max_length=10000, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('home', ['ChatLine'])

        # Adding model 'EditUserProfile'
        db.create_table('home_edituserprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(default=None, to=orm['auth.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('date_of_change', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('new_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
        ))
        db.send_create_signal('home', ['EditUserProfile'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('home_userprofile')

        # Removing M2M table for field following on 'UserProfile'
        db.delete_table('home_userprofile_following')

        # Removing M2M table for field chats on 'UserProfile'
        db.delete_table('home_userprofile_chats')

        # Deleting model 'PetReport'
        db.delete_table('home_petreport')

        # Removing M2M table for field workers on 'PetReport'
        db.delete_table('home_petreport_workers')

        # Removing M2M table for field bookmarked_by on 'PetReport'
        db.delete_table('home_petreport_bookmarked_by')

        # Deleting model 'PetMatch'
        db.delete_table('home_petmatch')

        # Removing M2M table for field up_votes on 'PetMatch'
        db.delete_table('home_petmatch_up_votes')

        # Removing M2M table for field down_votes on 'PetMatch'
        db.delete_table('home_petmatch_down_votes')

        # Deleting model 'Chat'
        db.delete_table('home_chat')

        # Deleting model 'ChatLine'
        db.delete_table('home_chatline')

        # Deleting model 'EditUserProfile'
        db.delete_table('home_edituserprofile')


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
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'null': 'True'}),
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
            'age': ('django.db.models.fields.CharField', [], {'default': "'Not Known'", 'max_length': '10', 'null': 'True'}),
            'bookmarked_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'bookmarks_related'", 'null': 'True', 'to': "orm['home.UserProfile']"}),
            'breed': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '30', 'null': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '30', 'null': 'True'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'date_lost_or_found': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '1000', 'null': 'True'}),
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
            'spayed_or_neutered': ('django.db.models.fields.CharField', [], {'default': "'Not Known'", 'max_length': '10', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5'}),
            'tag_info': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True'}),
            'thumb_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
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