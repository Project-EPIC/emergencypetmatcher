"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from reporting.models import Pets, PetReport
from matching.models import PetMatch, Chat, User
import random

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
		for i in range (self.NUMBER_OF_TESTS):

			chat = Chat(pet_report = PetReport(lost=True))
			chat.save()
			chat_same = Chat.objects.get(name = str(i))
			self.assertEqual(chat, chat_same)


	def test_updateChat(self):
		pass

	def test_deleteChat(self):

'''''''''''''''''''''''''''''''''''''''''''''''''''
CRUD Tests for: PetMatch 
'''''''''''''''''''''''''''''''''''''''''''''''''''

	#SAVE+READ Operation
	def test_savePetMatch(self):

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
	def test_readPetMatch(self):

		for i in range (self.NUMBER_OF_TESTS):

			#First, create the PetMatch object.
			pm = PetMatch.objects.create (	lost_pet = PetReport(lost = True), 
											found_pet = PetReport (lost = False), 
											proposed_by = User(name= "testUser"),
											score = i )

			pm_same = PetMatch.objects.get(score = i)

			#Assert that they are the same
			self.assertEqual(pm, pm_same)

			#UPDATE: score
			pm.score = i - 1

			#Save it to the database.
			pm.save()
			pm_updated = PetMatch.objects.get(score = i - 1)

			#Now assert that the updated PetMatch matches the one we've just updated.
			self.assertEqual(pm, pm_updated)


	def test_deletePetMatch(self):

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











