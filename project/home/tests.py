from home.models import *
from django.contrib.auth import authenticate
import unittest, string, random, sys, time
import test_utils as utils

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
ModelTesting: Testing for EPM Models
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
 		print '>>> Testing test_saveUser for %d iterations' % utils.NUMBER_OF_TESTS
 		iteration_time = 0.00

 		for i in range (utils.NUMBER_OF_TESTS):
 			start_time = time.clock()

			#Create the essential ingredients for the User object.
			#Creating a User creates a User Profile!
			user, password = utils.create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			# check we can find the user in the database again
			user_prof = UserProfile.objects.get(user = user)
			self.assertEquals(user_profile, user_prof)
			user = user_prof.user

			#Now, use the authenticate function
			self.assertTrue(user.check_password(password) == True)
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is not None)

			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)


	def test_updateUser (self):
		print '>>> Testing test_updateUser for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = utils.create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			# check that we can update the user's username
			changed_username = utils.generate_string (10) + str(i)
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

			utils.output_update (i + 1)		
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)

	def test_deleteUser(self):
		print '>>> Testing test_deleteUser for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = utils.create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			User.objects.get(username = username).delete()
			self.assertTrue(len(UserProfile.objects.all()) == 0)
			self.assertTrue(len(User.objects.all()) == 0)

			#Now, use the authenticate function
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is None)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(UserProfile.objects.all()) == 0)
		self.assertTrue(len(User.objects.all()) == 0)
		utils.performance_report(iteration_time)

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetReport
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_savePetReport(self):
		print '>>>> Testing test_savePetReport for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = utils.create_random_PetReport(user)
			
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
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)

	def test_updatePetReport(self):
		print '>>>> Testing test_updatePetReport for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = utils.create_random_PetReport(user)

			#UPDATES
			pr.pet_name = utils.generate_string (30)
			pr.description = utils.generate_string (300)
			pr.sex = random.choice(SEX_CHOICES)[0]
			pr.location = utils.generate_string (50)
			pr.color = utils.generate_string (20)
			pr.breed = utils.generate_string (30)
			pr.size = utils.generate_string (30)
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
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)

	def test_deletePetReport(self):
		print '>>>> Testing test_deletePetReport for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = utils.create_random_PetReport(user)

			PetReport.objects.get(proposed_by = user).delete()
			self.assertTrue(len(PetReport.objects.all()) == 0)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue (len(PetReport.objects.all()) == 0)
		utils.performance_report(iteration_time)


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetMatch 
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_savePetMatch(self):
		print '>>>> Testing test_savePetMatch for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = utils.create_random_User(i)
			user2, password2 = utils.create_random_User(i)
			user3, password3 = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport objects.
			pr1 = utils.create_random_PetReport(user2)
			pr2 = utils.create_random_PetReport(user3)

			#Now, create the PetMatch
			pm = utils.create_random_PetMatch(pr1, pr2, user)

			#Now, retrieve it and assert that they are the same.
			pm_same = PetMatch.objects.get(proposed_by = user.get_profile())
			self.assertEqual(pm.lost_pet, pm_same.lost_pet)
			self.assertEqual(pm.found_pet, pm_same.found_pet)
			self.assertEqual(pm.proposed_by, pm_same.proposed_by)
			self.assertEqual(pm, pm_same)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)


	def test_updatePetMatch(self):
		print '>>>> Testing test_updatePetMatch for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = utils.create_random_User(i)
			user2, password2 = utils.create_random_User(i)
			user3, password3 = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport objects.
			pr1 = utils.create_random_PetReport(user2)
			pr2 = utils.create_random_PetReport(user3)

			#Now, create the PetMatch
			pm = utils.create_random_PetMatch(pr1, pr2, user)

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
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)


	def test_deletePetMatch(self):
		print '>>>> Testing test_deletePetMatch for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = utils.create_random_User(i)
			user2, password2 = utils.create_random_User(i)
			user3, password3 = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport objects.
			pr1 = utils.create_random_PetReport(user2)
			pr2 = utils.create_random_PetReport(user3)

			#Now, create the PetMatch
			pm = utils.create_random_PetMatch(pr1, pr2, user)

			#And now delete the PetMatch Object.
			PetMatch.objects.all().get(proposed_by = user.get_profile(), lost_pet = pr1, found_pet = pr2).delete()
			#Assert that there is nothing in the database!
			self.assertTrue(len(PetMatch.objects.all()) == 0)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == 0)
		utils.performance_report(iteration_time)


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: Chat
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_saveChat(self):
		print '>>>> Testing test_saveChat for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()
			#Create the essential ingredients for the User object(s).
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object(s).
			pr = utils.create_random_PetReport(user)

			#Now, create the Chat Object.
			chat = utils.create_random_Chat(pr)

			# check we can find the Chat in the database again
			chat_same = Chat.objects.get(pet_report = pr)
			self.assertEqual(chat.pet_report, chat_same.pet_report)
			self.assertEqual(chat, chat_same)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)

	def test_updateChat(self):
		print '>>>> Testing test_updateChat for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()
			#Create the essential ingredients for the User object(s).
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object(s).
			pr = utils.create_random_PetReport(user)

			#Now, create the Chat Object.
			chat = utils.create_random_Chat(pr)

			#UPDATES
			user_profile = user.get_profile()
			user_profile.chats.add(chat)
			user_profile.save()

			# check we can find the Chat in the database again
			chat_same = Chat.objects.get(pet_report = pr)
			self.assertEqual(chat.pet_report, chat_same.pet_report)
			self.assertEqual(chat.userprofile_set.get(), chat_same.userprofile_set.get())
			self.assertEqual(chat, chat_same)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)


	def test_deleteChat(self):
		print '>>>> Testing test_deleteChat for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object(s).
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object(s).
			pr = utils.create_random_PetReport(user)

			#Now, create the Chat Object.
			chat = utils.create_random_Chat(pr)

			#Delete the Chat object.
			Chat.objects.get(pet_report = pr).delete()
			self.assertTrue(len(Chat.objects.all()) == 0)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(Chat.objects.all()) == 0)
		utils.performance_report(iteration_time)


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: ChatLine
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_saveChatLine(self):
		print '>>>> Testing test_saveChatLine for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()
			#Create the essential ingredients for the User object(s).
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object(s).
			pr = utils.create_random_PetReport(user)

			#Create the essential ingredients for the Chat object(s).
			chat = utils.create_random_Chat(pr)

			#Now, create the ChatLine Object.
			chatline = utils.create_random_ChatLine(user, chat)

			#Now, retrieve the chatline object.
			chatline_same = ChatLine.objects.get(chat = chat)
			self.assertEqual(chatline.chat, chatline_same.chat)
			self.assertEqual(chatline.userprofile, chatline_same.userprofile)
			self.assertEqual(chatline.text, chatline_same.text)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)

	def test_updateChatLine(self):
		print '>>>> Testing test_updateChatLine for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()
			#Create the essential ingredients for the User object(s).
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object(s).
			pr = utils.create_random_PetReport(user)

			#Create the essential ingredients for the Chat object(s).
			chat = utils.create_random_Chat(pr)

			#Now, create the ChatLine Object.
			chatline = utils.create_random_ChatLine(user, chat)

			#UPDATE
			chatline.text = utils.generate_string (10000)
			chatline.save()

			#Now, retrieve the chatline object.
			chatline_same = ChatLine.objects.get(chat = chat)
			self.assertEqual(chatline.chat, chatline_same.chat)
			self.assertEqual(chatline.userprofile, chatline_same.userprofile)
			self.assertEqual(chatline.text, chatline_same.text)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)

	def test_deleteChatLine(self):
		print '>>>> Testing test_deleteChatLine for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()
			#Create the essential ingredients for the User object(s).
			user, password = utils.create_random_User(i)

			#Create the essential ingredients for the PetReport object(s).
			pr = utils.create_random_PetReport(user)

			#Create the essential ingredients for the Chat object(s).
			chat = utils.create_random_Chat(pr)

			#Now, create the ChatLine Object.
			chatline = utils.create_random_ChatLine(user, chat)

			#Now, delete the ChatLine object
			ChatLine.objects.get(chat = chat).delete()
			self.assertTrue(len(ChatLine.objects.all()) == 0)
			utils.output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(UserProfile.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		self.assertTrue(len(ChatLine.objects.all()) == 0)
		utils.performance_report(iteration_time)


