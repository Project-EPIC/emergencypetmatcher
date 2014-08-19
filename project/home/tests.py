from django.contrib.auth import authenticate
from django.test.client import Client
from time import sleep
from selenium import webdriver
from pprint import pprint
from fixture import *
from django.template.loader import render_to_string
from project.settings import TEST_TWITTER_USER, TEST_TWITTER_PASSWORD, TEST_FACEBOOK_USER, TEST_FACEBOOK_PASSWORD, TEST_DOMAIN, EMAIL_FILE_PATH, EMAIL_BACKEND
from home.constants import *
from utilities.utils import *
import unittest, string, random, sys, time, urlparse, project.settings, math

'''===================================================================================
home.tests.py: Testing for Home App Functionality:

Test classes: home.ModelTesting home.LoginTesting home.LoggerTesting home.UserProfileTesting home.EditUserProfileTesting home.FollowingTesting home.HomePageTesting home.RegistrationTesting

Still need work:
home.SocialAuthTesting home.ReputationTesting
==================================================================================='''

'''===================================================================================
ModelTesting: Testing for EPM Models
==================================================================================='''
class ModelTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)
	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)

	#CRUD Tests for: UserProfile + User		
 	def test_save_User(self):
 		print_testing_name("test_save_User")
 		iteration_time = 0.00

 		for i in range (NUMBER_OF_TESTS):
 			start_time = time.clock()

			#Create the essential ingredients for the User object.
			#Creating a User creates a User Profile!
			user, password = create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randint(0,100)
			user_profile.save()

			# check we can find the user in the database again
			user_prof = UserProfile.objects.get(user = user)
			self.assertEquals(user_profile, user_prof)
			user = user_prof.user

			#Now, use the authenticate function
			self.assertTrue(user.check_password(password) == True)
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is not None)

			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)


	def test_update_User (self):
		print_testing_name("test_update_User")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randint(0,100)
			user_profile.save()

			# check that we can update the user's username
			changed_username = generate_string (10) + str(i)
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
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_delete_User(self):
		print_testing_name("test_delete_User")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randint(0,100)
			user_profile.save()

			User.objects.get(username = username).delete()
			self.assertTrue(len(UserProfile.objects.all()) == 0)
			self.assertTrue(len(User.objects.all()) == 0)

			#Now, use the authenticate function
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is None)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue(len(UserProfile.objects.all()) == 0)
		self.assertTrue(len(User.objects.all()) == 0)
		performance_report(iteration_time)

	
	#CRUD Tests for: UserProfile + User
	def test_save_PetReport(self):
		print_testing_name("test_save_PetReport")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = create_random_PetReport(user=user)
			
			print_debug_msg (user)
			# check we can find the PetReport in the database again
			pet_report = PetReport.objects.get(proposed_by=user)

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
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue (len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_update_PetReport(self):
		print_testing_name("test_update_PetReport")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = create_random_PetReport(user=user)

			#UPDATES
			pr.pet_name = generate_string (PETREPORT_PET_NAME_LENGTH)
			pr.description = generate_lipsum_paragraph(PETREPORT_DESCRIPTION_LENGTH)
			pr.sex = random.choice(SEX_CHOICES)[0]
			pr.location = generate_string (PETREPORT_LOCATION_LENGTH)
			pr.color = generate_string (PETREPORT_COLOR_LENGTH)
			pr.breed = generate_string (PETREPORT_BREED_LENGTH)
			pr.size = generate_string (PETREPORT_SIZE_LENGTH)
			pr.age = str(random.randint(0,15))

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
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue (len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_delete_PetReport(self):
		print_testing_name("test_delete_PetReport")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = create_random_PetReport(user=user)

			PetReport.objects.get(proposed_by=user).delete()
			self.assertTrue(len(PetReport.objects.all()) == 0)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(PetReport.objects.all()) == 0)
		performance_report(iteration_time)


	#CRUD Tests for: PetMatch 	
	def test_save_PetMatch(self):
		print_testing_name("test_save_PetMatch")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = create_random_User(str(i) + 'a')
			user2, password2 = create_random_User(str(i) + 'b')
			user3, password3 = create_random_User(str(i) + 'c')

			#Create the essential ingredients for the PetReport objects.
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
			pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)

			#Now, create the PetMatch
			pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)

			#Now, retrieve it and assert that they are the same.
			pm_same = PetMatch.objects.get(proposed_by = user.get_profile())
			self.assertEqual(pm.lost_pet, pm_same.lost_pet)
			self.assertEqual(pm.found_pet, pm_same.found_pet)
			self.assertEqual(pm.proposed_by, pm_same.proposed_by)
			self.assertEqual(pm, pm_same)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)


	def test_save_improperly_saved_PetMatch(self):
		print_testing_name("test_save_improperly_saved_PetMatch")
		iteration_time = 0.00

		start_time = time.clock()
		for i in range (NUMBER_OF_TESTS):

			create_random_User(str(i) + 'a')
			create_random_User(str(i) + 'b')
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr_lost = create_random_PetReport(status="Lost")
			pr_found = create_random_PetReport(status="Found")

			#Now, create an improperly-placed PetMatch (i.e. Lost on Found attribute, Found on Lost attribute).
			pm = create_random_PetMatch(lost_pet=pr_found, found_pet=pr_lost)

			self.assertEquals(pm, None)
			self.assertEquals(PetMatch.objects.filter(lost_pet=pr_found, found_pet=pr_lost).exists(), False)

			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == 0)
		performance_report(iteration_time)

	def test_save_duplicate_PetMatch(self):
		print_testing_name("test_save_duplicate_PetMatch")
		iteration_time = 0.00

		start_time = time.clock()
		for i in range (NUMBER_OF_TESTS):

			u1 = create_random_User(str(i) + 'a')
			u2 = create_random_User(str(i) + 'b')
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr_lost = create_random_PetReport(status="Lost")
			pr_found = create_random_PetReport(status="Found")
			pm = create_random_PetMatch(lost_pet=pr_lost, found_pet=pr_found, user = u1[0])
			pm_duplicate = create_random_PetMatch(lost_pet=pr_lost, found_pet=pr_found, user = u2[0])

			self.assertFalse(pm == None)
			self.assertEquals(pm_duplicate, None)
			self.assertEquals(PetMatch.objects.filter(lost_pet=pr_lost, found_pet=pr_found, proposed_by = u1[0]).exists(), True)			
			self.assertEquals(PetMatch.objects.filter(lost_pet=pr_lost, found_pet=pr_found, proposed_by = u2[0]).exists(), False)

			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)		


	def test_update_PetMatch(self):
		print_testing_name("test_update_PetMatch")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = create_random_User(str(i) + 'a')
			user2, password2 = create_random_User(str(i) + 'b')
			user3, password3 = create_random_User(str(i) + 'c')

			#Create the essential ingredients for the PetReport objects.
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
			pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)

			#Now, create the PetMatch
			pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)

			#UPDATES
			pm.down_votes = create_random_Userlist()
			pm.up_votes = create_random_Userlist()
			pm.is_successful = random.choice ([True, False])

			#Save it to the database.
			pm.save()
			pm_updated = PetMatch.objects.get(proposed_by = user.get_profile(), lost_pet = pr1, found_pet = pr2)

			#Now assert that the updated PetMatch matches the one we've just updated.
			self.assertEqual(pm, pm_updated)
			self.assertEqual(len(pm.down_votes.all()), len(pm_updated.down_votes.all()))
			self.assertEqual(len(pm.up_votes.all()), len(pm_updated.up_votes.all()))
			self.assertEqual(pm.is_successful, pm_updated.is_successful)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)


	def test_delete_PetMatch(self):
		print_testing_name("test_delete_PetMatch")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = create_random_User(str(i) + 'a')
			user2, password2 = create_random_User(str(i) + 'b')
			user3, password3 = create_random_User(str(i) + 'c')

			#Create the essential ingredients for the PetReport objects.
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
			pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)

			#Now, create the PetMatch
			pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)

			#And now delete the PetMatch Object.
			PetMatch.objects.all().get(proposed_by = user.get_profile(), lost_pet = pr1, found_pet = pr2).delete()
			#Assert that there is nothing in the database!
			self.assertTrue(len(PetMatch.objects.all()) == 0)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == 0)
		performance_report(iteration_time)


'''===================================================================================
LoginTesting: Testing for EPM logger In/Out
==================================================================================='''
class LoginTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_login_Users_successfully(self):
		print_testing_name("test_login_Users_successfully")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects()
		users = results ["users"]
		clients = results ["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Get the test objects.
			user, password = random.choice(users)
			client = random.choice(clients)

			print_test_msg("%s logs onto %s and attempts to login..." % (user.username, client))

			#Go to the Login Page
			response = client.get(URL_LOGIN)
			next = response.context ['next']
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request ['PATH_INFO'] == URL_LOGIN)
			self.assertTrue(next == URL_HOME)

			#Submit Login information
			response = client.post (URL_LOGIN, {'username': user.username, 'password': password, 'next': next}, follow=True)

			#Get Redirected back to the home page.
			self.assertTrue(response.status_code == 200)
			self.assertTrue(len(response.redirect_chain) == 1)
			self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
			self.assertTrue(response.redirect_chain[0][1] == 302)
			self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)
			client.logout()

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)


'''===================================================================================
SocialAuthTesting: Testing for Social Authentication
==================================================================================='''

# class SocialAuthTesting(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()
#         # pass

#     def url(self, path):
#         return urlparse.urljoin(TEST_DOMAIN, path)

#     def test_twitter_authentication(self):
#     	print_testing_name('test_twitter_authentication')
#         start_time = time.clock()

#         # Assert the username and passward for the testing Twitter account are not none
#         self.assertTrue(TEST_TWITTER_USER)
#         self.assertTrue(TEST_TWITTER_PASSWORD)

#         # Go to Twitter App Authorization page
#         self.driver.get(self.url('/login/twitter/'))
#         self.assertEqual("Twitter / Authorize an application", self.driver.title)
#         print_test_msg("Redirecting to log in Twitter App Authorization page.")

#         # Log in Twitter using the testing user credential
#         username_field = self.driver.find_element_by_id('username_or_email')
#         username_field.send_keys(TEST_TWITTER_USER)
#         password_field = self.driver.find_element_by_id('password')
#         password_field.send_keys(TEST_TWITTER_PASSWORD)
 
#         try:
#         	# Try to log in
#             password_field.submit()           
#             sleep(5)
        
# 	        # If the testing user is not found in the user profile table,
# 	        # the user will be prompted to submit a username 
#             try:
# 	        	assert "Social Account" in self.driver.title
# 	        	username_field = self.driver.find_element_by_id('username_id')
# 	        	# username = "twitter_test_user" + str(random.randrange(100, 999))
# 	        	username =  str(random.randrange(100, 999))
# 	        	username_field.send_keys(username)
# 	        	email_field = self.driver.find_element_by_id('email_id')
# 	         	email = "twitter_test_user@twitter.com"
# 	         	email_field.send_keys(email)
# 	         	# username_field.submit()	  
# 	         	self.driver.find_element_by_id("submit").click()
# 	         	# print "  Submitting a username '%s' for a created user profile account." % username
#             except:
#                 pass
	        
# 	        # Assert the user logged in and has been redirected to the app home page 
# 	        # after successful authentication by Twitter 
#             assert "EPM" in self.driver.title
#             self.assertTrue(self.driver.find_element_by_id('logout'))
#             print_test_msg("Successfully logger in EPM home page with Twitter authentication.")
#         except:
#         	print_test_msg("Unable to authenticate the testing user with Twitter.")

#         end_time = time.clock()
#         performance_report(end_time - start_time)
      


'''===================================================================================
LoggerTesting: Testing for EPM logger Activities
==================================================================================='''
class LoggerTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_create_activity_log(self):
		print_testing_name("test_create_activity_log")
		iteration_time = 0.00

		for i in range(NUMBER_OF_TESTS):
			start_time = time.clock()
			user = User.objects.create_user(username=generate_string(USER_USERNAME_LENGTH))
			userprofile = user.get_profile()

			#Now check: Does the userprofile's log file exist where it should?
			self.assertTrue(logger.log_exists(userprofile) == True)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)				


	def test_delete_objects_and_check_log (self):
		print_testing_name("test_delete_objects_and_check_log")
		iteration_time = 0.00

		results  = setup_objects(delete_all_objects=False, create_following_lists=True, create_petreports=True, create_petmatches=True)
		users = results ['users']
		clients = results ['clients']
		petreports = results ['petreports']
		petmatches = results ['petmatches']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			user, password = users.pop()
			client = random.choice(clients)
			petreport = petreports.pop()
			petmatch = None

			#Delete the objects.
			if len(petmatches) != 0:
				petmatch = petmatches.pop() 
				petmatch.delete()

			petreport.delete()

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg ("%s logs onto %s..." % (user, client))

			#We expect the system not to throw errors but to catch them.
			activities = logger.get_activities_from_log(userprofile=user.userprofile, current_userprofile=user.userprofile)
			activities += logger.get_bookmarking_activities_from_log(userprofile=user.userprofile)
			print_test_msg("%s has an activity feed list of size [%d]" % (user, len(activities)))
			self.assertTrue(logger.log_exists(user.userprofile))

			#Now, delete the user.
			user.delete()
			self.assertFalse(logger.log_exists(user.userprofile))

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)


	def test_log_account_creations(self):
		print_testing_name("test_log_account_creations")
		iteration_time = 0.00

		for i in range(NUMBER_OF_TESTS):
			start_time = time.clock()
			(user, password) = create_random_User(i)
			user_log_filename = ACTIVITY_LOG_DIRECTORY + str(user.get_profile().id) + ".log"

			with open(user_log_filename, 'r') as logging:

				lines = list(iter(logging.readlines()))
				print lines
				self.assertTrue(logger.activity_has_been_logged(ACTIVITY_ACCOUNT_CREATED, user.get_profile()) == True)
				self.assertEquals(len(lines), 1)

			logging.close()
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)		


	def test_log_submit_PetReport(self):
		print_testing_name("test_log_submit_PetReport")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False)
		users = results ['users']
		clients = results ['clients']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)

			#Create and submit a Pet Report object as form content
			pr = create_random_PetReport(user=user)

			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			pr_dict = model_to_dict(pr) 
			pr_dict ['img_path'] = None #Nullify the img_path attribute
			pr_dict ['pet_name'] = user.username + str(i)
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)

			#Make the POST request Call
			response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertTrue(len(response.redirect_chain) == 1) 
			self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)
			self.assertTrue(len(PetReport.objects.all()) == 2*i + 2)
			client.logout()

			#Now, check if the activity for submitting a PetReport appears in this user's log.
			petreport = PetReport.objects.get(proposed_by = user, pet_name = user.username + str(i))
			self.assertTrue(logger.activity_has_been_logged(ACTIVITY_PETREPORT_SUBMITTED, user.get_profile(), petreport=petreport) == True)	

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == 2*NUMBER_OF_TESTS) 
		performance_report(iteration_time)


	def test_log_propose_PetMatch (self):
		print_testing_name("test_log_propose_PetMatch")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_petreports=True)
		users = results ['users']
		clients = results ['clients']
		petreports = results ['petreports']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg ("%s logs onto %s to enter the matching interface..." % (user, client))			

			#Go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)
			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)

			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print_test_msg ("Oh! There are no PetReports to match this PetReport with - Back to the Home Page!")
				continue

			self.assertEquals(response.status_code, 200)
			print_test_msg ("%s has successfully requested page '%s'..." % (user, matching_url))
			candidate_petreport = random.choice(filtered_pet_reports) 

			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print_test_msg ("%s has successfully requested page '%s'..." % (user, propose_match_url))

			#Make the POST request Call		
			description = generate_lipsum_paragraph(500)
			post = {'description': description}
			response = client.post(propose_match_url, post, follow=True)
			client.logout()						

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(len(response.redirect_chain), 1)
			self.assertEquals(response.redirect_chain[0][0], 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertEquals(response.request ['PATH_INFO'], URL_HOME)		

			#Grab the PetMatch that has either been posted in the past or has been posted by this User.
			match = PetMatch.get_PetMatch(petreport, candidate_petreport)

			#Either the User is upvoting an already existing PetMatch...
			if match.UserProfile_has_voted(user.get_profile()) == UPVOTE:
				self.assertTrue(logger.activity_has_been_logged(ACTIVITY_PETMATCH_UPVOTE, user.get_profile(), petmatch=match) == True)
				print_test_msg ("A PetMatch already exists with these two PetReports, and so %s has up-voted this match!" % (user))

			#...Or the User successfully proposed a NEW PetMatch.
			else:
				self.assertTrue(logger.activity_has_been_logged(ACTIVITY_PETMATCH_PROPOSED, user.get_profile(), petmatch=match) == True)					
				print_test_msg ("%s has successfully POSTED a new match!" % (user))
	
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)		
		performance_report(iteration_time)

	def test_log_following_UserProfile(self):
		print_testing_name("test_log_following_UserProfile")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False)
		users = results ['users']
		clients = results ['clients']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			user_one, password_one = random.choice(users)
			user_two, password_two = random.choice(users)
			userprofile_one = user_one.get_profile()
			userprofile_two = user_two.get_profile()
			client = random.choice(clients)
			
			if user_one.id == user_two.id:
				continue

			#Log in First.
			loggedin = client.login(username = userprofile_one.user.username, password = password_one)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to follow %s." % (userprofile_one.user.username, client, userprofile_two.user.username))

			# Go to the second user's profile page
			response = client.get(URL_USERPROFILE + str(userprofile_two.id) + "/")
			self.assertEquals(response.status_code, 200)

			# Make the POST request Call for following the second user
			post = {'target_userprofile_id': userprofile_two.id}
			response = client.post(URL_FOLLOW, post, follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()						

			# Check if the activity for following a UserProfile appears in this userprofile_one's log.
			self.assertTrue(logger.activity_has_been_logged(ACTIVITY_FOLLOWING, userprofile=userprofile_one, userprofile2=userprofile_two) == True)		
			print_success_msg("%s has followed %s" % (userprofile_one.user.username, userprofile_two.user.username))

			# Check if the activity for following a UserProfile appears in this userprofile_two's log.
			self.assertTrue(logger.activity_has_been_logged(ACTIVITY_FOLLOWER, userprofile=userprofile_two, userprofile2=userprofile_one) == True)				
			print_success_msg("%s has been followed by %s" % (userprofile_two.user.username, userprofile_one.user.username))
	
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)		
		performance_report(iteration_time)


	def test_log_unfollowing_UserProfile(self):
		print_testing_name("test_log_unfollowing_UserProfile")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False)
		users = results ['users']
		clients = results ['clients']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			user_one, password_one = random.choice(users)
			user_two, password_two = random.choice(users)
			userprofile_one = user_one.get_profile()
			userprofile_two = user_two.get_profile()
			client = random.choice(clients)
			
			if user_one.id == user_two.id:
				continue

			#Log in First.
			loggedin = client.login(username = userprofile_one.user.username, password = password_one)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to follow %s." % (userprofile_one.user.username, client, userprofile_two.user.username))

			# Go to the second user's profile page
			response = client.get(URL_USERPROFILE + str(userprofile_two.id) + "/")
			self.assertEquals(response.status_code, 200)

			# Make the POST request Call for following the second user
			post = {'target_userprofile_id': userprofile_two.id}
			response = client.post(URL_FOLLOW, post, follow=True)
			self.assertEquals(response.status_code, 200)

			# Make the POST request Call for unfollowing the second user
			post = {'target_userprofile_id': userprofile_two.id}
			response = client.post(URL_UNFOLLOW, post, follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()						

			# Check if the activity for unfollowing a UserProfile appears in this userprofile_one's log.
			self.assertTrue(logger.activity_has_been_logged(ACTIVITY_UNFOLLOWING, userprofile=userprofile_one, userprofile2=userprofile_two) == True)			
			print_success_msg("%s has unfollowed %s" % (userprofile_one.user.username, userprofile_two.user.username))
				
			# Check if the activity for unfollowing a UserProfile appears in this userprofile_two's log.
			self.assertTrue(logger.activity_has_been_logged(ACTIVITY_UNFOLLOWER, userprofile=userprofile_two, userprofile2=userprofile_one) == True)			
			print_success_msg("%s has been unfollowed by %s" % (userprofile_two.user.username, userprofile_one.user.username))
				
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)		
		performance_report(iteration_time)


	def test_log_add_PetReport_bookmark(self):
		print_testing_name("test_log_add_PetReport_bookmark")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_petreports=True)
		users = results ["users"]
		clients = results ["clients"]
		petreports = results ["petreports"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)
			print_test_msg("A user %s and a pet report %s have been created." % (user.userprofile, petreport))

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the PRDP to add a bookmark." % (user, client))		

			# Go to the PRDP (Pet Report Detailed Page) interface
			response = client.get(URL_PRDP + str(petreport.id) + "/")
			self.assertEquals(response.status_code, 200)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			#if user has bookmarked this petreport previously,
			if(petreport.UserProfile_has_bookmarked(user.get_profile())):
				previously_bookmarked = True
			else:
				previously_bookmarked = False

			# Add a bookmark
			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()	
			new_bookmarks_count = user.get_profile().bookmarks_related.count()
			
			#Make assertions
			if not previously_bookmarked:
				self.assertEquals(old_bookmarks_count, (new_bookmarks_count-1))

			# Check if the activity for adding a PetReport bookmark appears in this user's log.
			print_test_msg("%s has added a bookmark for %s." % (user, petreport))
			self.assertTrue(logger.activity_has_been_logged(ACTIVITY_PETREPORT_ADD_BOOKMARK, userprofile=user.get_profile(), petreport=petreport) == True)

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)		
		performance_report(iteration_time)


	def test_log_remove_PetReport_bookmark(self):
		print_testing_name("test_log_remove_PetReport_bookmark")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_petreports=True)
		users = results ["users"]
		clients = results ["clients"]
		petreports = results ["petreports"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)
			print_test_msg("A user %s and a pet report %s have been created." % (user.userprofile, petreport))

			# Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the prdp interface to remove a bookmark." % (user, client))

			# Go to the PRDP (Pet Report Detailed Page) interface
			response = client.get(URL_PRDP + str(petreport.id) + "/")
			self.assertEquals(response.status_code, 200)

			# Add a bookmark
			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)	
			self.assertEquals(response.status_code, 200)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			# Remove the bookmark
			remove_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Remove Bookmark"}
			response = client.post(remove_bookmark_url, post, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
			self.assertEquals(response.status_code, 200)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()
			client.logout()	

			#Make assertions
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))

			# Check if the activity for adding a PetReport bookmark appears in this user's log.
			print_test_msg("%s has removed a bookmark for %s." % (user, petreport))
			self.assertTrue(logger.activity_has_been_logged(ACTIVITY_PETREPORT_ADD_BOOKMARK, userprofile=user.get_profile(), petreport=petreport) == True)				

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)		
		performance_report(iteration_time)


	def test_get_activities_json(self):
		print_testing_name("test_get_activities_json")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_following_lists=True, create_petreports=True, create_petmatches=True)
		users = results ["users"]
		clients = results ["clients"]
		petreports = results ["petreports"]
		petmatches = results ["petmatches"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			userprofile = user.get_profile()			
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg ("%s logs onto %s to enter the matching interface..." % (user, client))	

			#Request the get_activities_json view function()
			response = client.get(URL_GET_ACTIVITIES, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			client.logout()	

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], URL_GET_ACTIVITIES)

			#But now, let's test to get and assert those actual activities
			activities = []
			for following in userprofile.following.all().order_by("?")[:ACTIVITY_FEED_LENGTH]:
				activities += logger.get_activities_from_log(userprofile=following, current_userprofile=userprofile, since_date=userprofile.last_logout)				

			num_following = len(userprofile.following.all())
			num_activities = len(activities)
			print_test_msg("%s has %d followers and got an activity feed list of size %d when ACTIVITY_FEED_LENGTH = %d" % (user, num_following, num_activities, ACTIVITY_FEED_LENGTH))

			#Bounds checking
			self.assertTrue(num_activities >= 0)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)	


	def test_get_activities_json_for_anonymous_user(self):
		print_testing_name("test_get_activities_json_for_anonymous_user")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_following_lists=True, create_petreports=True, create_petmatches=True)
		users = results ["users"]
		clients = results ["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			client = random.choice(clients)
			
			#Request the get_activities_json view function()
			response = client.get(URL_GET_ACTIVITIES, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], URL_GET_ACTIVITIES)

			#But now, let's test to get and assert those actual activities
			activities = []
			for userprof in UserProfile.objects.order_by("?").filter(user__is_active=True)[:ACTIVITY_FEED_LENGTH]:
				activities += logger.get_activities_from_log(userprofile=userprof, current_userprofile=None, num_activities=1)			
			num_activities = len(activities)
			print_test_msg("The anonymous user got an activity feed list of size %d when the maximum length = %d" % (num_activities, ACTIVITY_FEED_LENGTH))

			#Bounds checking
			self.assertTrue(num_activities >= 0 and num_activities <= ACTIVITY_FEED_LENGTH)

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)		
		performance_report(iteration_time)	


	def test_get_activities_json_for_authenticated_user(self):
		print_testing_name("test_get_activities_json_for_authenticated_user")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_following_lists=True, create_petreports=True, create_petmatches=True)
		users = results ["users"]
		clients = results ["clients"]
		petreports = results ["petreports"]
		petmatches = results ["petmatches"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			userprofile = user.get_profile()
			another_user, another_user_password = random.choice(users)
			petreport = random.choice(petreports)
			client = random.choice(clients)

			if user.id == another_user.id:
				continue

			#Log into another_user.
			loggedin = client.login(username = another_user.username, password = another_user_password)
			self.assertTrue(loggedin == True)

			# Make the POST request Call for another_user to follow the user
			post = {'target_userprofile_id': user.userprofile.id}
			response = client.post(URL_FOLLOW, post, follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()	

			#Log into user.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)

			# Make the POST request Call for user to follow the another_user
			post = {'target_userprofile_id': another_user.userprofile.id}
			response = client.post(URL_FOLLOW, post, follow=True)
			self.assertEquals(response.status_code, 200)

			#Summing up the minimum value of user's activity feeds
			min_num_activities = len(userprofile.followers.all()) + len(userprofile.following.all())

			print_test_msg("Grabbing activities for %s with ID [%d]" % (userprofile.user.username, userprofile.id))
			
			#Request the get_activities_json view function()
			response = client.get(URL_GET_ACTIVITIES, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			client.logout()	

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], URL_GET_ACTIVITIES)

			#But now, let's test to get and assert those actual activities
			activities = []

			# Get all activities from this UserProfile's log file that show who has followed this UserProfile 
			follower_activities = logger.get_activities_from_log(userprofile=userprofile, current_userprofile=userprofile, activity=ACTIVITY_FOLLOWER, num_activities=10)

			for activity in activities:
				self.assertTrue(activity[1]["activity"] == ACTIVITY_FOLLOWER)
				self.assertTrue(activity[1]["current_userprofile_id"] == userprofile.id)		
			print_success_msg("Follower activities are good!")

			# Get all activities that associated to the PetReports I bookmarked
			bookmarked_activities = logger.get_bookmarking_activities_from_log(userprofile=userprofile, since_date=userprofile.last_logout, num_activities=10)

			for activity in bookmarked_activities:
				self.assertTrue(activity[1]["activity"] == ACTIVITY_PETREPORT_ADD_BOOKMARK or activity[0]["activity"] == ACTIVITY_PETREPORT_ADD_BOOKMARK)
				self.assertTrue(activity[1]["current_userprofile_id"] == userprofile.id)
			print_success_msg("Bookmarked activities are good!")	

			# Get all activities that are associated with the UserProfiles I follow
			following_activities = []
			for following in userprofile.following.all():
				following_activities += logger.get_activities_from_log(userprofile=following, current_userprofile=userprofile, since_date=userprofile.last_logout)

			for activity in following_activities:
				self.assertTrue(activity[1]["current_userprofile_id"] == str(userprofile.id))
			print_success_msg("Following activities are good!")				

			activities += follower_activities + following_activities + bookmarked_activities
			activities.sort()
			num_following = len(userprofile.following.all())
			num_activities = len(activities)
			print_test_msg ("%s has %d followers and got an activity feed list of size %d when the minimum length = %d" % (user, num_following, num_activities, min_num_activities))

			#Bounds checking
			self.assertTrue(num_activities >= min_num_activities)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)		
		performance_report(iteration_time)	


'''===================================================================================
HomePageTesting: Testing for the EPM Home Page
==================================================================================='''
class HomePageTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)	

	#Testing if the list of PetReports in the home page are ordered in reverse chronological fashion
	def test_get_PetReports(self):
		print_testing_name("test_homepage_get_PetReports")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(create_petreports=True)
		users = results ['users']
		clients = results ['clients']

		#Need to compute the number of "pages" (at least 1) that we can support given NUMBER_OF_TESTS.
		num_iterations = int(math.ceil(float(NUMBER_OF_TESTS)/NUM_PETREPORTS_HOMEPAGE))

		#Let's iterate through generated PetReports in pages
		for i in range (num_iterations):
			start_time = time.clock()

			#objects
			page = i + 1
			user, password = random.choice(users)
			client = random.choice(clients)

			response = client.get(URL_HOME)
			self.assertEquals(response.status_code, 200)
			url = URL_GET_PETREPORTS + "/" + str(page) + "/"
			response = client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ["PATH_INFO"], url)
			
			pet_reports = PetReport.objects.filter(closed = False).order_by("id").reverse()
			total_petreport_count = len(pet_reports)
			pet_reports = PetReport.get_PetReports_by_page(pet_reports, page)

			#Iterate through each paged PetReport and assert that it's ID is indeed the right one.
			for j in range(len(pet_reports)):
				petreport = pet_reports[j]
				expected_id = total_petreport_count - ((page-1) * NUM_PETREPORTS_HOMEPAGE) - j
				self.assertEquals(petreport.id, expected_id)
				print_success_msg("PetReport: %s == %d" % (petreport, expected_id))

			output_update(i + 1, iterations=num_iterations)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		performance_report(iteration_time)

	#Testing if the list of PetMatches in the home page are ordered in reverse chronological fashion
	def test_get_PetMatches(self):
		print_testing_name("test_get_PetMatches")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(create_petreports=True, create_petmatches=True)
		users = results ['users']
		clients = results ['clients']
		petmatches = results ["petmatches"]

		#Need to compute the number of "pages" (at least 1) that we can support given NUMBER_OF_TESTS.
		num_iterations = int(math.ceil(float(NUMBER_OF_TESTS)/NUM_PETMATCHES_HOMEPAGE))

		#Let's iterate through generated PetReports in pages
		for i in range (num_iterations):
			start_time = time.clock()

			#objects
			page = i + 1
			user, password = random.choice(users)
			client = random.choice(clients)

			response = client.get(URL_HOME)
			self.assertEquals(response.status_code, 200)
			url = URL_GET_PETMATCHES + "/" + str(page) + "/"
			response = client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ["PATH_INFO"], url)
			
			total_pet_matches = PetMatch.objects.filter(petcheck = None).order_by("id").reverse()
			total_petmatch_count = len(total_pet_matches)
			paged_pet_matches = PetMatch.get_PetMatches_by_page(total_pet_matches, page)

			#Iterate through each paged PetReport and assert that its ID is indeed the right one.
			for j in range(len(paged_pet_matches)):
				petmatch = paged_pet_matches[j]
				expected_id = total_petmatch_count - ((page-1) * NUM_PETMATCHES_HOMEPAGE) - j
				self.assertEquals(petmatch.id, expected_id)
				print_success_msg("%s =[id equals]= %d" % (petmatch, expected_id))

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		performance_report(iteration_time)

	#Testing if the list of PetMatches in the home page are ordered in reverse chronological fashion
	def test_get_successful_PetMatches(self):
		print_testing_name("test_get_successful_PetMatches")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(create_petreports=True, create_petmatches=True, allow_closed_matches=True)
		users = results ['users']
		clients = results ['clients']
		petmatches = results ["petmatches"]

		#Need to compute the number of "pages" (at least 1) that we can support given NUMBER_OF_TESTS.
		num_iterations = int(math.ceil(float(NUMBER_OF_TESTS)/NUM_PETMATCHES_HOMEPAGE))
		print_debug_msg("num_iterations: %s" % num_iterations)

		#Let's iterate through generated PetReports in pages
		for i in range (num_iterations):
			start_time = time.clock()

			#objects
			page = i + 1
			user, password = random.choice(users)
			client = random.choice(clients)

			response = client.get(URL_HOME)
			self.assertEquals(response.status_code, 200)
			url = URL_GET_SUCCESSFUL_PETMATCHES + "/" + str(page) + "/"
			response = client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ["PATH_INFO"], url)
			
			total_pet_matches = PetMatch.objects.filter(is_successful = True).order_by("id").reverse()
			total_petmatch_count = len(total_pet_matches)
			paged_pet_matches = PetMatch.get_PetMatches_by_page(total_pet_matches, page)

			#If the total num of successful petmatches is smaller than the number for each page, then assert we have the exact number in our paged petmatches.
			if total_petmatch_count <= NUM_PETMATCHES_HOMEPAGE:
				self.assertEquals(len(paged_pet_matches), total_petmatch_count)
				print_success_msg("paged_petmatch_count: %d == total_petmatch_count: %d" % (len(paged_pet_matches), total_petmatch_count))
				break

			#Otherwise, for each paged petmatch, assert that it's within paged boundaries
			else:
				for petmatch in paged_pet_matches:
						self.assertTrue(petmatch in total_pet_matches [((page-1) * NUM_PETMATCHES_HOMEPAGE):((page-1) * NUM_PETMATCHES_HOMEPAGE + NUM_PETMATCHES_HOMEPAGE)])
						print_success_msg("successful PetMatch within paged boundaries")				

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		performance_report(iteration_time)			

	#Cannot test reverse chronological order, but we can test exclusivity.
	def test_get_bookmarks(self):
		print_testing_name("test_get_bookmarks")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(create_bookmark_lists=True, create_petreports=True)
		users = results ['users']
		clients = results ['clients']
		pet_reports = results ["petreports"]

		#Here, we iterate through each user and his/her bookmarks list, every page of it.
		for i in range(NUMBER_OF_TESTS):
			user, password = random.choice(users)
			client = random.choice(clients)

			response = client.get(URL_HOME)
			self.assertEquals(response.status_code, 200)
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)

			#Need to compute the number of "pages" (at least 1) that we can support given NUMBER_OF_TESTS.
			num_iterations = int(math.ceil(float(NUMBER_OF_TESTS)/NUM_BOOKMARKS_HOMEPAGE))

			#Let's iterate through generated PetReports in pages
			for j in range (num_iterations):
				start_time = time.clock()
				page = j + 1

				url = URL_GET_BOOKMARKS + "/" + str(page) + "/"
				response = client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
				self.assertEquals(response.status_code, 200)
				self.assertEquals(response.request ["PATH_INFO"], url)

				all_bookmarks = user.get_profile().bookmarks_related.all()
				total_bookmark_count = len(all_bookmarks)
				paged_bookmarks = PetReport.get_bookmarks_by_page(all_bookmarks, page)

				#If the total num of bookmarks is smaller than the number for each page, then assert we have the exact number in our paged_bookmarks.
				if total_bookmark_count <= NUM_BOOKMARKS_HOMEPAGE:
					self.assertEquals(len(paged_bookmarks), total_bookmark_count)
					print_success_msg("paged_bookmark_count: %d == total_bookmark_count: %d" % (len(paged_bookmarks), total_bookmark_count))
					break

				#Otherwise, for each paged_bookmark, assert that it's within paged boundaries
				else:
					for bookmark in paged_bookmarks:
						self.assertTrue(bookmark in all_bookmarks [((page-1) * NUM_BOOKMARKS_HOMEPAGE):((page-1) * NUM_BOOKMARKS_HOMEPAGE + NUM_BOOKMARKS_HOMEPAGE)])
						print_success_msg("bookmarked PetReport within paged boundaries")

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		performance_report(iteration_time)		


'''===================================================================================
RegistrationTesting: Testing for EPM Registration
==================================================================================='''
class RegistrationTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)	

	def test_duplicate_email_register_User (self):
		print_testing_name("test_duplicate_email_register_User")
		iteration_time = 0.0

		results = setup_objects(create_users=False, create_clients=True)
		clients = results ['clients']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			client = random.choice(clients)

			print_test_msg("Some user logs onto %s to register for EPM" % client)

			response = client.get(URL_LOGIN)
			self.assertEquals(response.status_code, 200)
			response = client.get(URL_REGISTRATION)
			self.assertEquals(response.status_code, 200)

			#develop the post
			username = generate_string(10)
			first_name = generate_string(10)
			last_name = generate_string(15)
			email = generate_string(6) + "@test.com"
			guardian_email = generate_string(6) + "@testguardian.com"
			password = generate_string (10)
			date_of_birth = generate_random_birthdate()

			#Coverage: Let's assume that half of the time, a User account with that email already exists...
			chance = random.random()
			if (chance < .50):
				User.objects.create_user(username = generate_string(10) + "a", email = email, password = password)
				print_test_msg ("A User with the same email already exists...")

			response = client.post(URL_REGISTRATION, {	"username":username, 
														"email":email, 
														"tos": "true",
														"first_name": first_name,
														"last_name": last_name,
														"guardian_email":guardian_email, 
														"password1":password, 
														"password2":password, 
														"date_of_birth":date_of_birth}, follow=True)

			self.assertEquals(response.status_code, 200)

			if (chance < .50):
				self.assertEquals(response.request ["PATH_INFO"], URL_REGISTRATION)
			else:
				self.assertEquals(response.request ["PATH_INFO"], URL_HOME)

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)

	def test_duplicate_username_register_User (self):
		print_testing_name("test_duplicate_username_register_User")
		iteration_time = 0.0

		results = setup_objects(create_users=False, create_clients=True)
		clients = results ['clients']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			client = random.choice(clients)

			print_test_msg("Some user logs onto %s to register for EPM" % client)

			response = client.get(URL_LOGIN)
			self.assertEquals(response.status_code, 200)
			response = client.get(URL_REGISTRATION)
			self.assertEquals(response.status_code, 200)

			#develop the post
			username = generate_string(10)
			first_name = generate_string(10)
			last_name = generate_string(15)
			email = generate_string(6) + "@test.com"
			guardian_email = generate_string(6) + "@testguardian.com"
			password = generate_string (10)
			date_of_birth = generate_random_birthdate()

			#Coverage: Let's assume that half of the time, a User account with that username already exists...
			chance = random.random()
			if (chance < .50):
				User.objects.create_user(username = username, email = generate_string(10), password = password)
				print_test_msg ("A User with the same username already exists...")

			response = client.post(URL_REGISTRATION, {	"username":username, 
														"email":email, 
														"tos": "true",
														"first_name": first_name,
														"last_name": last_name,
														"guardian_email":guardian_email, 
														"password1":password, 
														"password2":password, 
														"date_of_birth":date_of_birth}, follow=True)

			self.assertEquals(response.status_code, 200)

			if (chance < .50):
				self.assertEquals(response.request ["PATH_INFO"], URL_REGISTRATION)
			else:
				self.assertEquals(response.request ["PATH_INFO"], URL_HOME)

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)

	def test_inconsistent_passwords_register_User (self):
		print_testing_name("test_inconsistent_passwords_register_User")
		iteration_time = 0.0

		results = setup_objects(create_users=False, create_clients=True)
		clients = results ['clients']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			client = random.choice(clients)

			print_test_msg("Some user logs onto %s to register for EPM" % client)

			response = client.get(URL_LOGIN)
			self.assertEquals(response.status_code, 200)
			response = client.get(URL_REGISTRATION)
			self.assertEquals(response.status_code, 200)

			#develop the post
			username = generate_string(10)
			email = generate_string(6) + "@test.com"
			password1 = generate_string (10)
			password2 = password1
			first_name = generate_string(10)
			last_name = generate_string(15)
			guardian_email = generate_string(6) + "@testguardian.com"
			date_of_birth = generate_random_birthdate()

			#Coverage: Let's assume that half of the time, the passwords don't align...
			chance = random.random()
			if (chance < .50):
				print_test_msg ("Whoops, passwords do not match.")
				password2 = password1 + "a"
			
			response = client.post(URL_REGISTRATION, {	"username":username, 
														"email":email, 
														"tos": "true",
														"first_name": first_name,
														"last_name": last_name,
														"guardian_email":guardian_email, 
														"password1":password1, 
														"password2":password2, 
														"date_of_birth":date_of_birth}, follow=True)

			self.assertEquals(response.status_code, 200)

			if (chance < .50):
				self.assertEquals(response.request ["PATH_INFO"], URL_REGISTRATION)
			else:
				self.assertEquals(response.request ["PATH_INFO"], URL_HOME)

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)






































