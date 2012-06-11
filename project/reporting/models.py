from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager
from auth.models import User
from matching.models import Chat,PetMatch

class PetReport(models.Model):
    pet_type = models.CharField(max_length=30,null=False)
    pet_name=models.CharField(max_length=30,null=True) 
    lost = models.BooleanField()
    author = EmbeddedModelField(User,null=False) 
    color = models.CharField(max_length=20,null=False)
    age = models.IntegerField(null=True)
    breed = models.CharField(max_length=30,null=True)
    description   = models.CharField(max_length=300,null=True)
    SEX_CHOICES=(
		('m','Male'),
		('f','Female'),
		)
    sex = models.CharField(max_length=6,choices=SEX_CHOICES)
    date_lostOrFound = models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=25,null=False)
    size = models.CharField(max_length=30)
    revision = models.IntegerField(null=True) #update revision using view
    proposed_matches=ListField(EmbeddedModelField(PetMatch,null=True))
    workers = models.ListField(EmbeddedModelField(User,null=True))
    chat=EmbeddedModelField(Chat,null=True)


    def __unicode__(self):
	return u'{ %s lost:%s contact: %s}' % (self.pet_type,self.lost,self.author)

