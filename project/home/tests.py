"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from home.models import *
from django.contrib.auth import authenticate
import unittest, string, random, sys

#Control Variable
NUMBER_OF_TESTS = 100

def generate_string (size, chars = string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for i in range(size))

#Keep the user/tester updated.
def output_update (i):	
	output = "%d of %d iterations complete" % (i, NUMBER_OF_TESTS)
	sys.stdout.write("\r\x1b[K"+output.__str__())
	sys.stdout.flush()

def performance_report(total_time):
	print 'Total Time: %s sec' % (total_time)
	print 'AVG Time Taken for a Single Test: %s sec' % (total_time/NUMBER_OF_TESTS)


class ModelTesting (unittest.TestCase):

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

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: UserProfile + User
	'''''''''''''''''''''''''''''''''''''''''''''''''''
 	def test_saveUser(self):
 		print '>>> Testing test_saveUser for %d iterations' % NUMBER_OF_TESTS

 		for i in range (NUMBER_OF_TESTS):

			#Create the essential ingredients for the User object.
 			username = generate_string(10) + str(i)
		   	password = generate_string(10)
		   	email = generate_string(10) + '@' + 'test.com'
		   	first_name = generate_string(20)
		   	last_name = generate_string(20)

		   	#Creating a User creates a User Profile
			user = User(username = username, email = email, password = password, first_name = first_name, last_name = last_name)
			user.set_password (password)
			user.save()

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			# check we can find the user in the database again
			user_prof = UserProfile.objects.get(user = user)
			self.assertEquals(user_profile, user_prof)

			user = user_prof.user
			self.assertEquals(user.username, username)
			self.assertEquals(user.email, email)

			#Now, use the authenticate function
			self.assertTrue(user.check_password(password) == True)
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is not None)

			output_update (i + 1)

		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		print ''


	def test_updateUser (self):
		print '>>> Testing test_updateUser for %d iterations' % NUMBER_OF_TESTS

		for i in range (NUMBER_OF_TESTS):

			#Create the essential ingredients for the User object.
			username = generate_string(10) + str(i)
		   	password = generate_string(10)
		   	email = generate_string(10) + '@' + 'test.com'
		   	first_name = generate_string(20)
		   	last_name = generate_string(20)

		   	#Creating a User creates a User Profile
			user = User(username = username, email = email, password = password, first_name = first_name, last_name = last_name)
			user.set_password (password)
			user.save()

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			# check that we can read the saved User and update its username
			changed_username = generate_string(10) + str(i)
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
			self.assertTrue(user.check_password(password) == True)
			userObject = authenticate (username = changed_username, password = password)
			self.assertTrue(userObject is not None)

			output_update (i + 1)

		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		print ''

	def test_deleteUser(self):
		print '>>> Testing test_deleteUser for %d iterations' % NUMBER_OF_TESTS

		for i in range (NUMBER_OF_TESTS):

			#Create the essential ingredients for the User object.
			username = generate_string(10) + str(i)
		   	password = generate_string(10)
		   	email = generate_string(10) + '@' + 'test.com'
		   	first_name = generate_string(20)
		   	last_name = generate_string(20)

		   	#Creating a User creates a User Profile
			user = User(username = username, email = email, password = password, first_name = first_name, last_name = last_name)
			user.set_password (password)
			user.save()

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			User.objects.get(username = username).delete()
			self.assertTrue(len(UserProfile.objects.all()) == 0)
			self.assertTrue(len(User.objects.all()) == 0)

			#Now, use the authenticate function
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is None)

			output_update(i + 1)

		self.assertTrue(len(UserProfile.objects.all()) == 0)
		self.assertTrue(len(User.objects.all()) == 0)
		print ''

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetReport
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_savePetReport(self):
		print '>>>> Testing test_savePetReport for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']

		for i in range (NUMBER_OF_TESTS):

			#Create the essential ingredients for the PetReport object.
			pet_type = random.choice(choices)
			status = u'%s' % (random.choice(LOST_OR_FOUND_CHOICES)[0])
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)

			pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
			pr.pet_name = generate_string(30)
			pr.description = generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = generate_string(50)
			pr.color = generate_string(20)
			pr.breed = generate_string(30)
			pr.size = generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save() 

			# check we can find the PetReport in the database again
			pet_report = PetReport.objects.get(proposed_by = user)
			self.assertEquals(pr.proposed_by, pet_report.proposed_by)
			self.assertEquals(pr.pet_type, pet_report.pet_type)
			self.assertEquals(pr.status, pet_report.status)
			self.assertEquals(pr.description, pet_report.description)
			self.assertEquals(pr.sex, pet_report.sex)
			self.assertEquals(pr.location, pet_report.location)
			self.assertEquals(pr.color, pet_report.color)
			self.assertEquals(pr.breed, pet_report.breed)
			self.assertEquals(pr.size, pet_report.size)
			self.assertEquals(pr.age, pet_report.age)

			output_update (i + 1)

		self.assertTrue (len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		print ''

	def test_updatePetReport(self):
		print '>>>> Testing test_updatePetReport for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]

		for i in range (NUMBER_OF_TESTS):

			#Create the essential ingredients for the PetReport object.
			pet_type = random.choice(choices)
			status = u'%s' % (random.choice(LOST_OR_FOUND_CHOICES)[0])
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
			pr.pet_name = generate_string(30)
			pr.description = generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = generate_string(50)
			pr.color = generate_string(20)
			pr.breed = generate_string(30)
			pr.size = generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			#UPDATES
			pr.pet_name = generate_string(30)
			pr.description = generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = generate_string(50)
			pr.color = generate_string(20)
			pr.breed = generate_string(30)
			pr.size = generate_string(30)
			pr.age = random.randrange(0,15)

			# check we can find the PetReport in the database again
			pr.save()
			pet_report = PetReport.objects.get(proposed_by = user)

			self.assertEquals(pr.proposed_by, pet_report.proposed_by)
			self.assertEquals(pr.pet_type, pet_report.pet_type)
			self.assertEquals(pr.status, pet_report.status)
			self.assertEquals(pr.description, pet_report.description)
			self.assertEquals(pr.sex, pet_report.sex)
			self.assertEquals(pr.location, pet_report.location)
			self.assertEquals(pr.color, pet_report.color)
			self.assertEquals(pr.breed, pet_report.breed)
			self.assertEquals(pr.size, pet_report.size)
			self.assertEquals(pr.age, pet_report.age)

			output_update (i + 1)

		self.assertTrue (len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		print ''

	def test_deletePetReport(self):
		print '>>>> Testing test_deletePetReport for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]

		for i in range (NUMBER_OF_TESTS):

			#Create the essential ingredients for the PetReport object.
			pet_type = random.choice(choices)
			status = u'%s' % (random.choice(LOST_OR_FOUND_CHOICES)[0])
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
			pr.pet_name = generate_string(30)
			pr.description = generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = generate_string(50)
			pr.color = generate_string(20)
			pr.breed = generate_string(30)
			pr.size = generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			PetReport.objects.get(proposed_by = user).delete()
			self.assertTrue(len(PetReport.objects.all()) == 0)

			output_update (i + 1)

		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(PetReport.objects.all()) == 0)
		print ''


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetMatch 
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_savePetMatch(self):
		print '>>>> Testing test_savePetMatch for %d iterations' % NUMBER_OF_TESTS
		
		choices = ['dog', 'cat', 'turtle', 'other']
		for i in range (NUMBER_OF_TESTS):

			#First, create the essential ingredients for the PetMatch object.
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user1 = User.objects.create_user(username = username, email = email, password = password)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user2 = User.objects.create_user(username = username, email = email, password = password)
			pr1 = PetReport.objects.create (pet_type = random.choice(choices), status = random.choice([True,False]), 
				proposed_by = user1.get_profile())
			pr2 = PetReport.objects.create (pet_type = random.choice(choices), status = random.choice([True,False]), 
				proposed_by = user2.get_profile())
			pm = PetMatch ( lost_pet = pr1, found_pet = pr2, proposed_by = user.get_profile())
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])
			pm.save()

			#Now, retrieve it and assert that they are the same.
			pm_same = PetMatch.objects.get(proposed_by = user.get_profile())
			self.assertEqual(pm.lost_pet, pm_same.lost_pet)
			self.assertEqual(pm.found_pet, pm_same.found_pet)
			self.assertEqual(pm.proposed_by, pm_same.proposed_by)
			self.assertEqual(pm, pm_same)

			output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == NUMBER_OF_TESTS)
		print ''


	def test_updatePetMatch(self):
		print '>>>> Testing test_updatePetMatch for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		for i in range (NUMBER_OF_TESTS):

			#First, create the essential ingredients for the PetMatch object.
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user1 = User.objects.create_user(username = username, email = email, password = password)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user2 = User.objects.create_user(username = username, email = email, password = password)
			pr1 = PetReport.objects.create (pet_type = random.choice(choices), status = random.choice([True,False]), 
				proposed_by = user1.get_profile())
			pr2 = PetReport.objects.create (pet_type = random.choice(choices), status = random.choice([True,False]), 
				proposed_by = user2.get_profile())
			pm = PetMatch ( lost_pet = pr1, found_pet = pr2, proposed_by = user.get_profile())
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])
			pm.save()

			#UPDATES
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])

			#Save it to the database.
			pm.save()
			pm_updated = PetMatch.objects.get(proposed_by = user.get_profile(), lost_pet = pr1, found_pet = pr2)

			#Now assert that the updated PetMatch matches the one we've just updated.
			self.assertEqual(pm, pm_updated)
			self.assertEqual(pm.score, pm_updated.score)
			self.assertEqual(pm.is_open, pm_updated.is_open)

			output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == NUMBER_OF_TESTS)
		print ''


	def test_deletePetMatch(self):
		print '>>>> Testing test_deletePetMatch for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		for i in range (NUMBER_OF_TESTS):

			#First, create the essential ingredients for the PetMatch object.
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user1 = User.objects.create_user(username = username, email = email, password = password)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user2 = User.objects.create_user(username = username, email = email, password = password)
			pr1 = PetReport.objects.create (pet_type = random.choice(choices), status = random.choice([True,False]), 
				proposed_by = user1.get_profile())
			pr2 = PetReport.objects.create (pet_type = random.choice(choices), status = random.choice([True,False]), 
				proposed_by = user2.get_profile())
			pm = PetMatch ( lost_pet = pr1, found_pet = pr2, proposed_by = user.get_profile())
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])
			pm.save()

			PetMatch.objects.all().get(proposed_by = user.get_profile(), lost_pet = pr1, found_pet = pr2).delete()

			output_update(i + 1)

			#Assert that there is nothing in the database!
			self.assertTrue(len(PetMatch.objects.all()) == 0)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == 0)
		print ''


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: Chat
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_saveChat(self):
		print '>>>> Testing test_saveChat for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]
		for i in range(NUMBER_OF_TESTS):

			#Create the essential ingredients for the Chat object.
			pet_type = random.choice(choices)
			status = random.choice(lostOrTrue)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
			pr.pet_name = generate_string(30)
			pr.description = generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = generate_string(50)
			pr.color = generate_string(20)
			pr.breed = generate_string(30)
			pr.size = generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			chat = Chat(pet_report = pr)
			chat.save()

			# check we can find the Chat in the database again
			chat_same = Chat.objects.get(pet_report = pr)
			self.assertEqual(chat.pet_report, chat_same.pet_report)
			self.assertEqual(chat, chat_same)

			output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == NUMBER_OF_TESTS)
		print ''

	def test_updateChat(self):
		print '>>>> Testing test_updateChat for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]
		for i in range(NUMBER_OF_TESTS):

			#Create the essential ingredients for the Chat object.
			pet_type = random.choice(choices)
			status = random.choice(lostOrTrue)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
			pr.pet_name = generate_string(30)
			pr.description = generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = generate_string(50)
			pr.color = generate_string(20)
			pr.breed = generate_string(30)
			pr.size = generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			chat = Chat(pet_report = pr)
			chat.save()

			#UPDATES
			user_profile = user.get_profile()
			user_profile.chats.add(chat)
			user_profile.save()

			# check we can find the Chat in the database again
			chat_same = Chat.objects.get(pet_report = pr)
			self.assertEqual(chat.pet_report, chat_same.pet_report)
			self.assertEqual(chat.userprofile_set.get(), chat_same.userprofile_set.get())
			self.assertEqual(chat, chat_same)

			output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == NUMBER_OF_TESTS)
		print ''


	def test_deleteChat(self):
		print '>>>> Testing test_deleteChat for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		sex = ['Male', 'Female']
		lostOrTrue = [True, False]
		for i in range(NUMBER_OF_TESTS):

			#Create the essential ingredients for the Chat object.
			pet_type = random.choice(choices)
			status = random.choice(lostOrTrue)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
			pr.pet_name = generate_string(30)
			pr.description = generate_string(300)
			pr.sex = random.choice(sex)
			pr.location = generate_string(50)
			pr.color = generate_string(20)
			pr.breed = generate_string(30)
			pr.size = generate_string(30)
			pr.age = random.randrange(0,15)
			pr.save()

			chat = Chat(pet_report = pr)
			chat.save()

			#Delete the Chat object.
			Chat.objects.get(pet_report = pr).delete()
			self.assertTrue(len(Chat.objects.all()) == 0)

			output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == 0)
		print ''


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: ChatLine
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_saveChatLine(self):
		print '>>>> Testing test_saveChatLine for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		lostOrTrue = [True, False]
		for i in range(NUMBER_OF_TESTS):

			#Create the essential ingredients for the ChatLine object.
			pet_type = random.choice(choices)
			status = random.choice(lostOrTrue)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			pr = PetReport.objects.create(pet_type = pet_type, status = status, proposed_by = user.get_profile())
			chat = Chat.objects.create(pet_report = pr)

			chatline = ChatLine(chat = chat, userprofile = user.get_profile(), text = generate_string(10000))
			chatline.save()

			#Now, retrieve the chatline object.
			chatline_same = ChatLine.objects.get(chat = chat)
			self.assertEqual(chatline.chat, chatline_same.chat)
			self.assertEqual(chatline.userprofile, chatline_same.userprofile)
			self.assertEqual(chatline.text, chatline_same.text)

			output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == NUMBER_OF_TESTS)
		print ''

	def test_updateChatLine(self):
		print '>>>> Testing test_updateChatLine for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		lostOrTrue = [True, False]
		for i in range(NUMBER_OF_TESTS):

			#Create the essential ingredients for the ChatLine object.
			pet_type = random.choice(choices)
			status = random.choice(lostOrTrue)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			pr = PetReport.objects.create(pet_type = pet_type, status = status, proposed_by = user.get_profile())
			chat = Chat.objects.create(pet_report = pr)

			chatline = ChatLine(chat = chat, userprofile = user.get_profile(), text = generate_string(10000))
			chatline.save()

			#UPDATE
			chatline.text = generate_string(10000)
			chatline.save()

			#Now, retrieve the chatline object.
			chatline_same = ChatLine.objects.get(chat = chat)
			self.assertEqual(chatline.chat, chatline_same.chat)
			self.assertEqual(chatline.userprofile, chatline_same.userprofile)
			self.assertEqual(chatline.text, chatline_same.text)

			output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == NUMBER_OF_TESTS)
		print ''

	def test_deleteChatLine(self):
		print '>>>> Testing test_deleteChatLine for %d iterations' % NUMBER_OF_TESTS

		choices = ['dog', 'cat', 'turtle', 'other']
		lostOrTrue = [True, False]
		for i in range(NUMBER_OF_TESTS):

			#Create the essential ingredients for the ChatLine object.
			pet_type = random.choice(choices)
			status = random.choice(lostOrTrue)
			username = generate_string(10) + str(i)
			password = generate_string(10)
			email = generate_string(10) + '@' + 'test.com'
			user = User.objects.create_user(username = username, email = email, password = password)
			pr = PetReport.objects.create(pet_type = pet_type, status = status, proposed_by = user.get_profile())
			chat = Chat.objects.create(pet_report = pr)

			chatline = ChatLine(chat = chat, userprofile = user.get_profile(), text = generate_string(10000))
			chatline.save()

			#Now, delete the ChatLine object
			ChatLine.objects.get(chat = chat).delete()
			self.assertTrue(len(ChatLine.objects.all()) == 0)

			output_update(i + 1)

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == 0)
		print ''


