"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from home.models import *
from django.contrib.auth import authenticate
import unittest, string, random, sys
#sys.path.append('')

class MatchingTesting (unittest.TestCase):

	#Control Variable
	NUMBER_OF_TESTS = 100

	def generate_string (self, size, chars = string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for i in range(size))

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		User.objects.all().delete()
		UserProfile.objects.all().delete()
		PetMatch.objects.all().delete()
		PetReport.objects.all().delete()
		Chat.objects.all().delete()
		ChatLine.objects.all().delete()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		User.objects.all().delete()
		UserProfile.objects.all().delete()
		PetMatch.objects.all().delete()
		PetReport.objects.all().delete()
		Chat.objects.all().delete()
		ChatLine.objects.all().delete()

	#Keep the user/tester updated.
	def output_update (self, i):	
		output = "%d of %d iterations complete" % (i, self.NUMBER_OF_TESTS)
		sys.stdout.write("\r\x1b[K"+output.__str__())
		sys.stdout.flush()