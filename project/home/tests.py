"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from home.models import *
from django.contrib.auth import authenticate
import unittest, string, random, sys

class ModelTesting (unittest.TestCase):

	#Control Variable
	NUMBER_OF_TESTS = 100

	#User Vars
	USERNAME = None
	PASSWORD = None
	FIRST_NAME = None
	LAST_NAME = None
	EMAIL = None

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


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: UserProfile + User
	'''''''''''''''''''''''''''''''''''''''''''''''''''
 	def test_saveUser(self):
 		print '>>> Testing test_saveUser for %d iterations' % self.NUMBER_OF_TESTS

 		for i in range (self.NUMBER_OF_TESTS):

 			self.USERNAME = self.generate_string(10)
		   	self.PASSWORD = self.generate_string(10)
		   	self.EMAIL = self.generate_string(6) + '@' + 'test.com'

			user = User.objects.create_user(username = self.USERNAME, email = self.EMAIL, password = self.PASSWORD)
			user_profile = UserProfile (user = user)
			user_profile.save()

			# check we can find the user in the database again
			user_prof = UserProfile.objects.get(user = user)
			self.assertEquals(user_profile, user_prof)

			user = user_prof.user
			self.assertEquals(user.username, self.USERNAME)
			self.assertEquals(user.email, self.EMAIL)

			#Now, use the authenticate function
			userObject = authenticate (username = self.USERNAME, password = self.PASSWORD)
			self.assertTrue(userObject is not None)

			self.output_update (i + 1)

		self.assertTrue (len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == self.NUMBER_OF_TESTS)
		print ''


	def test_updateUser (self):
		print '>>> Testing test_updateUser for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			self.USERNAME = self.generate_string(10)
			self.PASSWORD = self.generate_string(10)
			self.EMAIL = self.generate_string(6) + '@' + 'test.com'
			user = User.objects.create_user(username = self.USERNAME, email = self.EMAIL, password = self.PASSWORD)
			user_profile = UserProfile (user = user)
			user_profile.save()

			# check that we can read the saved User and update its username
			changed_username = self.generate_string(10)
			user_profile = UserProfile.objects.get(user = user)
			user = user_profile.user

			self.assertTrue (user.username, self.USERNAME)
			user.username = changed_username
			user.save()

			user_profile = UserProfile.objects.get(user = user)
			user = user_profile.user
			self.assertEqual (user.username, changed_username)
			self.assertNotEqual (user.username, self.USERNAME)

			#Now, use the authenticate function
			userObject = authenticate (username = changed_username, password = self.PASSWORD)
			self.assertTrue(userObject is not None)

			self.output_update (i + 1)

		self.assertTrue (len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == self.NUMBER_OF_TESTS)
		print ''

	def test_deleteUser(self):
		print '>>> Testing test_deleteUser for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			self.USERNAME = self.generate_string(10)
			self.PASSWORD = self.generate_string(10)
			self.EMAIL = self.generate_string(6) + '@' + 'test.com'
			user = User.objects.create_user(username = self.USERNAME, email = self.EMAIL, password = self.PASSWORD)
			user_profile = UserProfile (user = user)
			user_profile.save()

			UserProfile.objects.get(user = user).delete()
			User.objects.get(username = self.USERNAME).delete()
			self.assertTrue(len(UserProfile.objects.all()) == 0)
			self.assertTrue(len(User.objects.all()) == 0)

			#Now, use the authenticate function
			userObject = authenticate (username = self.USERNAME, password = self.PASSWORD)
			self.assertTrue(userObject is None)

			self.output_update(i)

		self.assertTrue(len(UserProfile.objects.all()) == 0)
		self.assertTrue(len(User.objects.all()) == 0)


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetMatch 
	'''''''''''''''''''''''''''''''''''''''''''''''''''

	#SAVE+READ Operation
	def test_savePetMatch(self):
		print '>>>> Testing test_savePetMatch for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			#First, create the PetMatch object.
			pm = PetMatch ( lost_pet = PetReport(lost = True), 
							found_pet = PetReport (lost = False), 
							proposed_by = User(name= "testUser"),
							score = i )

			#Save it to the database.
			pm.save()

			#Now, retrieve it and assert that they are the same.
			pm_same = PetMatch.objects.get(score = i)
			self.assertEqual(pm, pm_same)

		self.assertTrue(len(PetMatch.objects.all()) == self.NUMBER_OF_TESTS)



	#UPDATE Operation
	def test_updatePetMatch(self):
		print '>>>> Testing test_updatePetMatch for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			#First, create and save the PetMatch object.
			pm = PetMatch.objects.create (	lost_pet = PetReport(lost = True), 
			found_pet = PetReport (lost = False), 
			proposed_by = User(name= "testUser"),
			score = i )

			#UPDATE: score
			pm.score = i - 1

			#Save it to the database.
			pm.save()
			pm_updated = PetMatch.objects.get(score = i - 1)

			#Now assert that the updated PetMatch matches the one we've just updated.
			self.assertEqual(pm, pm_updated)
			self.assertEqual(pm.score, pm_updated.score)


	def test_deletePetMatch(self):
		print '>>>> Testing test_deletePetMatch for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			#First, create the PetMatch object.
			pm = PetMatch.objects.create (	lost_pet = PetReport(lost = True), 
			found_pet = PetReport (lost = False), 
			proposed_by = User(name= "testUser"),
			score = i )

			PetMatch.objects.all().get(score = i).delete()

			#Assert that there is nothing in the database!
			self.assertTrue(len(PetMatch.objects.all()) == 0)

		self.assertTrue(len(PetMatch.objects.all()) == 0)


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetReport
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_savePetReport(self):
		print '>>>> Testing test_savePetReport for %d iterations' % self.NUMBER_OF_TESTS

		user1=User.objects.create()
		user1.name="User1"
		user1.save()
		self.dog=PetReport.objects.create(pet_type="dog",pet_name="Jackie",author=user1,
		lost=True,color='brown',breed="Labrador",sex='f',location="Boulder",size="1 foot tall")
		self.dog.save()

		print "unicode: "+self.dog+"\n"
		self.dog.description="Shaggy dog"

		self.assertEqual(self.dog.pet_type,"dog")
		self.assertEqual(self.dog.pet_name,"Jackie")



	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: Chat
	'''''''''''''''''''''''''''''''''''''''''''''''''''

	def test_saveChat(self):
		print '>>>> Testing test_saveChat for %d iterations' % self.NUMBER_OF_TESTS

		for i in range(self.NUMBER_OF_TESTS):

			#First, create the User and PetReport objects to correctly create and save the Chat Object.
			user = User (	username = self.USERNAME + str(i),
							password = self.PASSWORD,
							first_name = self.FIRST_NAME,
							last_name = self.LAST_NAME )
							#email = self.EMAIL )

			pr = PetReport(pet_type = "Dog", lost = True, proposed_by = user)
		#	chat = Chat(pet_report = pr)
		#	chat.current_users.append(user)
		#	chat.save()

			#Bring out the Chat Object by its User's first name.
		#	chat_same = Chat.objects.get()
		#	self.assertEqual(chat, chat_same)
		#	self.assertEqual(chat.pet_report, chat_same.pet_report)

		#self.assertTrue(len(Chat.objects.all()) == self.NUMBER_OF_TESTS)

	def test_updateChat(self):
		print '>>>> Testing test_updateChat for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			#First, create the Chat object
			pr = PetReport(lost=True)
			chat = Chat.objects.create(pet_report = pr)

			#UPDATE: chat content
			chatContent = chat.content
			self.assertTrue(len(chatContent) == 0)
			chatContent.append({'user': User(name="testUser"), 
			'content': "TEST_CONTENT", 'date': datetime.datetime.now()})

			#Save it to the database.
			chat.save()
			chat_updated = Chat.objects.get(name = str(i - 1))

			#Now assert that the updated Chat matches the one we've just updated.
			self.assertEqual(chat, chat_updated)


	def test_deleteChat(self):
		print '>>>> Testing test_deleteChat for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			#First, create the Chat object.
			pm = Chat.objects.create ( name = str(i), pet_report = PetReport(lost=True))

			#Delete that (specific) one.
			Chat.objects.all().get(name = str(i)).delete()

			#Assert that there is nothing in the database!
			self.assertTrue(len(Chat.objects.all()) == 0)

		self.assertTrue(len(Chat.objects.all()) == 0)


