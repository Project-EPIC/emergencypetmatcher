from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager
from reporting.models import PetReport, Pets

# Create your models here.

class User (models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)

#The Pet Match Object Model
class PetMatch(models.Model):
	lost_pet = EmbeddedModelField(PetReport)
	found_pet = EmbeddedModelField(PetReport)
	proposed_by = EmbeddedModelField(User)
	is_open = models.BooleanField()
	#It is OK that this field is null (initially)
	up_votes = ListField(EmbeddedModelField(User), null=True)
	down_votes = ListField(EmbeddedModelField(User), null=True)
	score = models.IntegerField(null=True)
	closed_by = EmbeddedModelField(User, null=True)

	def __unicode__ (self):
		return '{objid: %s - %s:%s }' % (self.id, self.lost_pet, self.found_pet)


#The Chat Object Model
class Chat (models.Model):
	name = models.CharField(max_length=100)
	pet_report = EmbeddedModelField(PetReport)
	current_users = ListField(EmbeddedModelField(User))
	#content has a List of Lists of [User, text, date]
	content = ListField(ListField(EmbeddedModelField(User), 
		models.CharField(blank=False), models.DateTimeField()))