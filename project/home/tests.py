"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from django.test import TestCase
from home.models import *

class ModelTesting (unittest.TestCase):

	#Control Variable
	NUMBER_OF_TESTS = 100

	#User Vars
	USERNAME = "TEST_USER_NAME"
	PASSWORD = "TEST_PASSWORD"
	FIRST_NAME = "TEST_FIRST_NAME"
	LAST_NAME = "TEST_LAST_NAME"
	EMAIL = "TEST@TEST.COM"
	

	def setUp(self):
		#Get rid of all objects in the QuerySet.
		User.objects.all().delete()
		PetMatch.objects.all().delete()
		PetReport.objects.all().delete()
		Chat.objects.all().delete()


	def tearDown(self):
		#Get rid of all objects in the QuerySet.
		User.objects.all().delete()
		PetMatch.objects.all().delete()
		PetReport.objects.all().delete()
		Chat.objects.all().delete()

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: User
	'''''''''''''''''''''''''''''''''''''''''''''''''''
 	def test_saveUser(self):
 		self.user.save()


	def test_reading_user_from_database(self):

    	# check we can find the user in the database again
		all_users = User.objects.all()
		self.assertEquals(len(all_users), 1)
		only_user = all_users[0]
		self.assertEquals(only_user, self.user)

		# check that its correct attributes are retrieved:
		self.assertEquals(only_user.userid, 1)
		self.assertEquals(only_user.username, 'user1')
		self.assertEquals(only_user.password, '1234') 

		# or ..................................
		#temp_user = User.objects.get(pk=1) ???
		temp_user = User.objects.get(userid=1)
		self.assertEquals(temp_user.username, 'user1')
		self.assertEquals(temp_user.password, '1234')
		self.assertEquals(temp_user.first_name, 'Ken')
		self.assertEquals(temp_user.last_name, 'Anderson')
		self.assertEquals(temp_user.email, 'ken.anderson@gmail.com')
		self.assertEquals(temp_user.rebutation, 0)



	def test_updateUser(self):
		# check we can update the user's attibutes
		self.user.first_name = 'Sahar'
		self.assertNotEquals(self.user.first_name, 'Ken')
		self.assertEquals(self.user.first_name, 'Sahar')

		# or do we need to read in temp_user
		temp_user = User.objects.get(userid=1)
		temp_user.last_name = 'Jambi'
		self.assertNotEquals(temp_user.last_name, 'Anderson')
		self.assertEquals(temp_user.last_name, 'Jambi')

		# try to update the user's friends embedded list
		user2 = User.objects.create(userid=22)
		user3 = User.objects.create()
		#user2.save()
		#user3.save()
		temp_user.friends = [user2, user3]
		self.assertEquals(temp_user.friends, [user2, user3])

		# try to update the user's working_on pets embedded list
		pet1 = Pet.objects.create()
		pet2 = Pet.objects.create()
		temp_user.working_on = [pet1]
		self.assertEquals(temp_user.working_on, [pet1])
		self.assertNotEquals(temp_user.working_on, [pet2])


	def test_deleteUser(self):
		# check we can delete the user
		self.user.delete()
		all_users = User.objects.all()
		self.assertEquals(len(all_users), 0)


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

			user = User (	username = self.TEST_USER_NAME,
							password = self.PASSWORD,
							first_name = self.TEST_FIRST_NAME,
							last_name = self.TEST_LAST_NAME,
							email = self.EMAIL )
			
			pr = PetReport(lost=True)
			chat = Chat(pet_report = pr)
			chat.save()
			chat_same = Chat.objects.get(pet_report=pr)
			self.assertEqual(chat, chat_same)
			self.assertEqual(chat.pet_report, chat_same.pet_report)

		self.assertTrue(len(Chat.objects.all()) == self.NUMBER_OF_TESTS)

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


