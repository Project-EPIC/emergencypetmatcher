"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from reporting.models import Pets, PetReport
from matching.models import PetMatch, Chat, User
import random, datetime

class MatchingTest(TestCase):

	#Control Variable
	NUMBER_OF_TESTS = 100

	def setUp(self):
		#Get rid of all objects in the QuerySet.
		PetMatch.objects.all().delete()
		Chat.objects.all().delete()

	def tearDown(self):
		#Get rid of all objects in the QuerySet.
		PetMatch.objects.all().delete()
		Chat.objects.all().delete()

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: Chat
	'''''''''''''''''''''''''''''''''''''''''''''''''''

	def test_saveChat(self):
		print '>>>> Testing test_saveChat for %d iterations' % self.NUMBER_OF_TESTS

		for i in range(self.NUMBER_OF_TESTS):

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

		pass

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetMatch 
	'''''''''''''''''''''''''''''''''''''''''''''''''''

	#SAVE+READ Operation
	def test_savePetMatch(self):
		print '>>>> Testing test_savePetMatch for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			#First, create the PetMatch object.
			pm = PetMatch(	lost_pet = PetReport(lost = True), 
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











