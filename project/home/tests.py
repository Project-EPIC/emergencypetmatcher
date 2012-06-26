"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from home.models import *
from django.contrib.auth import authenticate
import unittest, string, random, sys
#sys.path.append('')


def start_test(self):
	print 'hello there'

class ModelTesting (unittest.TestCase):

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


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: UserProfile + User
	'''''''''''''''''''''''''''''''''''''''''''''''''''
 	def test_saveUser(self):
 		print '>>> Testing test_saveUser for %d iterations' % self.NUMBER_OF_TESTS

 		for i in range (self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the User object.
 			username = self.generate_string(10)
		   	password = self.generate_string(10)
		   	email = self.generate_string(6) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			user_profile = UserProfile (user = user)
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			# check we can find the user in the database again
			user_prof = UserProfile.objects.get(user = user)
			self.assertEquals(user_profile, user_prof)

			user = user_prof.user
			self.assertEquals(user.username, username)
			self.assertEquals(user.email, email)

			#Now, use the authenticate function
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is not None)

			self.output_update (i + 1)

		self.assertTrue (len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == self.NUMBER_OF_TESTS)
		print ''


	def test_updateUser (self):
		print '>>> Testing test_updateUser for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):


			#Create the essential ingredients for the User object.
			username = self.generate_string(10)
		   	password = self.generate_string(10)
		   	email = self.generate_string(6) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			user_profile = UserProfile (user = user)
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			# check that we can read the saved User and update its username
			changed_username = self.generate_string(10)
			user_profile = UserProfile.objects.get(user = user)
			user = user_profile.user

			self.assertTrue (user.username, username)
			user.username = changed_username
			user.save()

			user_profile = UserProfile.objects.get(user = user)
			user = user_profile.user
			self.assertEqual (user.username, changed_username)
			self.assertNotEqual (user.username, username)

			#Now, use the authenticate function
			userObject = authenticate (username = changed_username, password = password)
			self.assertTrue(userObject is not None)

			self.output_update (i + 1)

		self.assertTrue (len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == self.NUMBER_OF_TESTS)
		print ''

	def test_deleteUser(self):
		print '>>> Testing test_deleteUser for %d iterations' % self.NUMBER_OF_TESTS

		for i in range (self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the User object.
			username = self.generate_string(10)
		   	password = self.generate_string(10)
		   	email = self.generate_string(6) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			user_profile = UserProfile (user = user)
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			UserProfile.objects.get(user = user).delete()
			User.objects.get(username = username).delete()
			self.assertTrue(len(UserProfile.objects.all()) == 0)
			self.assertTrue(len(User.objects.all()) == 0)

			#Now, use the authenticate function
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is None)

			self.output_update(i + 1)

		self.assertTrue(len(UserProfile.objects.all()) == 0)
		self.assertTrue(len(User.objects.all()) == 0)
		print ''

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetReport
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_savePetReport(self):
		print '>>>> Testing test_savePetReport for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]

		for i in range (self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the PetReport object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport (pet_type = pet_type, lost = lost, proposed_by = user)
			pr.pet_name = self.generate_string(30)
			pr.description = self.generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = self.generate_string(50)
			pr.color = self.generate_string(20)
			pr.breed = self.generate_string(30)
			pr.size = self.generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			# check we can find the PetReport in the database again
			pet_report = PetReport.objects.get(proposed_by = user)
			self.assertEquals(pr.proposed_by, pet_report.proposed_by)
			self.assertEquals(pr.pet_type, pet_report.pet_type)
			self.assertEquals(pr.lost, pet_report.lost)
			self.assertEquals(pr.description, pet_report.description)
			self.assertEquals(pr.sex, pet_report.sex)
			self.assertEquals(pr.location, pet_report.location)
			self.assertEquals(pr.color, pet_report.color)
			self.assertEquals(pr.breed, pet_report.breed)
			self.assertEquals(pr.size, pet_report.size)
			self.assertEquals(pr.age, pet_report.age)

			self.output_update (i + 1)

		self.assertTrue (len(PetReport.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == self.NUMBER_OF_TESTS)
		print ''

	def test_updatePetReport(self):
		print '>>>> Testing test_updatePetReport for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]

		for i in range (self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the PetReport object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport (pet_type = pet_type, lost = lost, proposed_by = user)
			pr.pet_name = self.generate_string(30)
			pr.description = self.generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = self.generate_string(50)
			pr.color = self.generate_string(20)
			pr.breed = self.generate_string(30)
			pr.size = self.generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			#UPDATES
			pr.pet_name = self.generate_string(30)
			pr.description = self.generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = self.generate_string(50)
			pr.color = self.generate_string(20)
			pr.breed = self.generate_string(30)
			pr.size = self.generate_string(30)
			pr.age = random.randrange(0,15)

			# check we can find the PetReport in the database again
			pr.save()
			pet_report = PetReport.objects.get(proposed_by = user)

			self.assertEquals(pr.proposed_by, pet_report.proposed_by)
			self.assertEquals(pr.pet_type, pet_report.pet_type)
			self.assertEquals(pr.lost, pet_report.lost)
			self.assertEquals(pr.description, pet_report.description)
			self.assertEquals(pr.sex, pet_report.sex)
			self.assertEquals(pr.location, pet_report.location)
			self.assertEquals(pr.color, pet_report.color)
			self.assertEquals(pr.breed, pet_report.breed)
			self.assertEquals(pr.size, pet_report.size)
			self.assertEquals(pr.age, pet_report.age)

			self.output_update (i + 1)

		self.assertTrue (len(PetReport.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == self.NUMBER_OF_TESTS)
		print ''

	def test_deletePetReport(self):
		print '>>>> Testing test_deletePetReport for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]

		for i in range (self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the PetReport object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport (pet_type = pet_type, lost = lost, proposed_by = user)
			pr.pet_name = self.generate_string(30)
			pr.description = self.generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = self.generate_string(50)
			pr.color = self.generate_string(20)
			pr.breed = self.generate_string(30)
			pr.size = self.generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			PetReport.objects.get(proposed_by = user).delete()
			self.assertTrue(len(PetReport.objects.all()) == 0)

			self.output_update (i + 1)

		self.assertTrue (len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue (len(PetReport.objects.all()) == 0)
		print ''


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetMatch 
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_savePetMatch(self):
		print '>>>> Testing test_savePetMatch for %d iterations' % self.NUMBER_OF_TESTS
		
		choices = ['dog', 'cat', 'turtle', 'other']
		for i in range (self.NUMBER_OF_TESTS):

			#First, create the essential ingredients for the PetMatch object.
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user1 = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user2 = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			pr1 = PetReport.objects.create (pet_type = random.choice(choices), lost = random.choice([True,False]), 
				proposed_by = user1)
			pr2 = PetReport.objects.create (pet_type = random.choice(choices), lost = random.choice([True,False]), 
				proposed_by = user2)
			pm = PetMatch ( lost_pet = pr1, found_pet = pr2, proposed_by = user)
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])
			pm.save()

			#Now, retrieve it and assert that they are the same.
			pm_same = PetMatch.objects.get(proposed_by = user)
			self.assertEqual(pm.lost_pet, pm_same.lost_pet)
			self.assertEqual(pm.found_pet, pm_same.found_pet)
			self.assertEqual(pm.proposed_by, pm_same.proposed_by)
			self.assertEqual(pm, pm_same)

			self.output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == self.NUMBER_OF_TESTS)
		print ''


	def test_updatePetMatch(self):
		print '>>>> Testing test_updatePetMatch for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		for i in range (self.NUMBER_OF_TESTS):

			#First, create the essential ingredients for the PetMatch object.
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user1 = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user2 = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			pr1 = PetReport.objects.create (pet_type = random.choice(choices), lost = random.choice([True,False]), 
				proposed_by = user1)
			pr2 = PetReport.objects.create (pet_type = random.choice(choices), lost = random.choice([True,False]), 
				proposed_by = user2)
			pm = PetMatch ( lost_pet = pr1, found_pet = pr2, proposed_by = user)
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])
			pm.save()

			#UPDATES
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])

			#Save it to the database.
			pm.save()
			pm_updated = PetMatch.objects.get(proposed_by = user, lost_pet = pr1, found_pet = pr2)

			#Now assert that the updated PetMatch matches the one we've just updated.
			self.assertEqual(pm, pm_updated)
			self.assertEqual(pm.score, pm_updated.score)
			self.assertEqual(pm.is_open, pm_updated.is_open)

			self.output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == self.NUMBER_OF_TESTS)
		print ''


	def test_deletePetMatch(self):
		print '>>>> Testing test_deletePetMatch for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		for i in range (self.NUMBER_OF_TESTS):

			#First, create the essential ingredients for the PetMatch object.
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user1 = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user2 = UserProfile.objects.create(user = User.objects.create_user(username = username,
				email = email, password = password))
			pr1 = PetReport.objects.create (pet_type = random.choice(choices), lost = random.choice([True,False]), 
				proposed_by = user1)
			pr2 = PetReport.objects.create (pet_type = random.choice(choices), lost = random.choice([True,False]), 
				proposed_by = user2)
			pm = PetMatch ( lost_pet = pr1, found_pet = pr2, proposed_by = user)
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])
			pm.save()

			PetMatch.objects.all().get(proposed_by = user, lost_pet = pr1, found_pet = pr2).delete()

			self.output_update(i + 1)

			#Assert that there is nothing in the database!
			self.assertTrue(len(PetMatch.objects.all()) == 0)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == 0)
		print ''


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: Chat
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_saveChat(self):
		print '>>>> Testing test_saveChat for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]
		for i in range(self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the Chat object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport (pet_type = pet_type, lost = lost, proposed_by = user)
			pr.pet_name = self.generate_string(30)
			pr.description = self.generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = self.generate_string(50)
			pr.color = self.generate_string(20)
			pr.breed = self.generate_string(30)
			pr.size = self.generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			chat = Chat(pet_report = pr)
			chat.save()

			# check we can find the Chat in the database again
			chat_same = Chat.objects.get(pet_report = pr)
			self.assertEqual(chat.pet_report, chat_same.pet_report)
			self.assertEqual(chat, chat_same)

			self.output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == self.NUMBER_OF_TESTS)
		print ''

	def test_updateChat(self):
		print '>>>> Testing test_updateChat for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]
		for i in range(self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the Chat object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport (pet_type = pet_type, lost = lost, proposed_by = user)
			pr.pet_name = self.generate_string(30)
			pr.description = self.generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = self.generate_string(50)
			pr.color = self.generate_string(20)
			pr.breed = self.generate_string(30)
			pr.size = self.generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			chat = Chat(pet_report = pr)
			chat.save()

			#UPDATES
			user.chats.add(chat)
			user.save()

			# check we can find the Chat in the database again
			chat_same = Chat.objects.get(pet_report = pr)
			self.assertEqual(chat.pet_report, chat_same.pet_report)
			self.assertEqual(chat.userprofile_set.get(), chat_same.userprofile_set.get())
			self.assertEqual(chat, chat_same)

			self.output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == self.NUMBER_OF_TESTS)
		print ''


	def test_deleteChat(self):
		print '>>>> Testing test_deleteChat for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]
		for i in range(self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the Chat object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport (pet_type = pet_type, lost = lost, proposed_by = user)
			pr.pet_name = self.generate_string(30)
			pr.description = self.generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = self.generate_string(50)
			pr.color = self.generate_string(20)
			pr.breed = self.generate_string(30)
			pr.size = self.generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			chat = Chat(pet_report = pr)
			chat.save()

			#Delete the Chat object.
			Chat.objects.get(pet_report = pr).delete()
			self.assertTrue(len(Chat.objects.all()) == 0)

			self.output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == 0)
		print ''


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: ChatLine
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_saveChatLine(self):
		print '>>>> Testing test_saveChatLine for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		lostOrTrue = [True, False]
		for i in range(self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the ChatLine object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user_profile = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport.objects.create(pet_type = pet_type, lost = lost, proposed_by = user_profile)
			chat = Chat.objects.create(pet_report = pr)

			chatline = ChatLine(chat = chat, userprofile = user_profile, text = self.generate_string(10000))
			chatline.save()

			#Now, retrieve the chatline object.
			chatline_same = ChatLine.objects.get(chat = chat)
			self.assertEqual(chatline.chat, chatline_same.chat)
			self.assertEqual(chatline.userprofile, chatline_same.userprofile)
			self.assertEqual(chatline.text, chatline_same.text)

			self.output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == self.NUMBER_OF_TESTS)
		print ''

	def test_updateChatLine(self):
		print '>>>> Testing test_updateChatLine for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		lostOrTrue = [True, False]
		for i in range(self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the ChatLine object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user_profile = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport.objects.create(pet_type = pet_type, lost = lost, proposed_by = user_profile)
			chat = Chat.objects.create(pet_report = pr)

			chatline = ChatLine(chat = chat, userprofile = user_profile, text = self.generate_string(10000))
			chatline.save()

			#UPDATE
			chatline.text = self.generate_string(10000)
			chatline.save()

			#Now, retrieve the chatline object.
			chatline_same = ChatLine.objects.get(chat = chat)
			self.assertEqual(chatline.chat, chatline_same.chat)
			self.assertEqual(chatline.userprofile, chatline_same.userprofile)
			self.assertEqual(chatline.text, chatline_same.text)

			self.output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == self.NUMBER_OF_TESTS)
		print ''

	def test_deleteChatLine(self):
		print '>>>> Testing test_deleteChatLine for %d iterations' % self.NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		lostOrTrue = [True, False]
		for i in range(self.NUMBER_OF_TESTS):

			#Create the essential ingredients for the ChatLine object.
			pet_type = random.choice(choices)
			lost = random.choice(lostOrTrue)
			username = self.generate_string(10)
			password = self.generate_string(10)
			email = self.generate_string(6) + '@' + 'test.com'
			user_profile = UserProfile.objects.create(user = User.objects.create_user(username = username,
			 email = email, password = password))
			pr = PetReport.objects.create(pet_type = pet_type, lost = lost, proposed_by = user_profile)
			chat = Chat.objects.create(pet_report = pr)

			chatline = ChatLine(chat = chat, userprofile = user_profile, text = self.generate_string(10000))
			chatline.save()

			#Now, delete the ChatLine object
			ChatLine.objects.get(chat = chat).delete()
			self.assertTrue(len(ChatLine.objects.all()) == 0)

			self.output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == self.NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == self.NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == 0)
		print ''


