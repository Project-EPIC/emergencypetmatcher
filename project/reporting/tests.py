"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from reporting.models import PetReport
from auth.models import User
from matching.models import *
#import datetime

class SimpleTest(TestCase):
    def setUp(self):
	PetReport.objects.all().delete()
	User.objects.all().delete()
	Chat.objects.all().delete()
	PetMatch.objects.all().delete()
	
    def tearDown(self):
	PetReport.objects.all().delete()
	User.objects.all().delete()
	Chat.objects.all().delete()
	PetMatch.objects.all().delete()

    def test_petreports(self):
	user1=User.objects.create()
	user1.name="User1"
	user1.save()
	self.dog=PetReport.objects.create(pet_type="dog",pet_name="Jackie",author=user1,lost=True,color='brown',breed="Labrador",sex='f',location="Boulder",size="1 foot tall")
	self.dog.save()
	
	print "unicode: "+self.dog+"\n"
	self.dog.description="Shaggy dog"
	
    	self.assertEqual(self.dog.pet_type,"dog")
    	self.assertEqual(self.dog.pet_name,"Jackie")
	
    	

