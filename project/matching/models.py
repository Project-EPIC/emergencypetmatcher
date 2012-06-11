from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField
from django_mongodb_engine.contrib import MongoDBManager
from reporting.models import PetReport, Pets

# Create your models here.

#The Pet Match Object Model
class PetMatch(models.Model):
	lost_pet = EmbeddedModelField(PetReport, null=False)
	found_pet = EmbeddedModelField(PetReport, null=False)
	proposed_by = EmbeddedModelField(User, null=False)
	proposed_date = models.DateTimeField(auto_now_add = True)
	is_open = models.BooleanField(default=True)
	#It is OK that this field is null (initially)
	up_votes = ListField(EmbeddedModelField(User), null=True)
	down_votes = ListField(EmbeddedModelField(User), null=True)
	score = models.IntegerField(default = 0)
	closed_by = EmbeddedModelField(User, null=True)
	closed_date = models.DateTimeField(null=True)

	def __unicode__ (self):
		return 'PetMatch {%s:%s}' % (self.lost_pet, self.found_pet)

#The Chat Object Model
class Chat (models.Model):
	pet_report = EmbeddedModelField(PetReport, null=False)
	current_users = ListField(EmbeddedModelField(User), null=True)
	#content has a List of DictFields of {User, text, date+time}. Note that the auto_now option means that
	#once a dictfield has been added or edited to this object instance, the date and time is recorded here.
	content = ListField(DictField(EmbeddedModelField(User, null=False), 
		models.CharField(max_length=1000, blank=True), models.DateTimeField(auto_now_add=True)))

	def __unicode__ (self):
		return 'Chat {pet_report:%s}' % (self.pet_report)

