"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from home.models import *
from django.contrib.auth import authenticate
import string, random, sys
import os


class RandomObjects:

	#Number of pet reprts to render
	NUMBER_OF_OBJECTS=30

	#User Vars
	USERNAME = None
	PASSWORD = None
	FIRST_NAME = None
	LAST_NAME = None
	EMAIL = None

	def generate_string (self, size, chars = string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for i in range(size))

	#Get rid of all objects in the QuerySet.
	def delete_all(self):
		User.objects.all().delete()
		UserProfile.objects.all().delete()
		PetMatch.objects.all().delete()
		PetReport.objects.all().delete()
		Chat.objects.all().delete()
		ChatLine.objects.all().delete()

	#Keep the user/tester updated.
	def output_update (self, i):#Do I need this method???	
		output = "%d of %d iterations complete" % (i, self.NUMBER_OF_OBJECTS)
		sys.stdout.write("\r\x1b[K"+output.__str__())
		sys.stdout.flush()


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	Create a UserProfile object
	'''''''''''''''''''''''''''''''''''''''''''''''''''
 	def create_User(self):
		USERNAME = self.generate_string(10)
		PASSWORD = self.generate_string(10)
		EMAIL = self.generate_string(6) + '@' + 'test.com'
		user = User.objects.create_user(username = USERNAME, email = EMAIL, password = PASSWORD)
		user_profile = UserProfile (user = user)
		user_profile.save()
		return user_profile

	
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	Create Objects for: PetReport
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def create_PetReports(self):
		#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
		user_profile = self.create_User()
		#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
		#zrint "Number of Objects: "+NUMBER_OF_OBJECTS
		print "\nSelf.NumberofObjects: "+str(self.NUMBER_OF_OBJECTS) 
		for i in range (self.NUMBER_OF_OBJECTS):
			dog=PetReport.objects.create(pet_type = "dog", pet_name = self.generate_string(10),proposed_by = user_profile, lost = True,color = 'brown',breed = "Labrador",sex ='f',location = "Boulder",size = "1 foot tall")
			dog.save()
			print str(dog)+'\n'
		
		for j in range (self.NUMBER_OF_OBJECTS):
			cat=PetReport.objects.create(pet_type = "cat", pet_name = self.generate_string(10),proposed_by = user_profile,lost = False,color = 'white',sex = 'm',location = "Denver",size = "small")
			cat.save()
		pet_reports_list = PetReport.objects.all()
		for pet in pet_reports_list:
			print str(pet)	
X = RandomObjects()
X.create_PetReports()