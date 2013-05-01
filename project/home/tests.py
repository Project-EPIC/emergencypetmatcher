from django.contrib.auth import authenticate
from django.test.client import Client
from django.contrib.sites.models import Site
from constants import *
from home.models import *
from logging import *
from utils import *
from time import sleep
from selenium import webdriver
from django.template.loader import render_to_string
from project.settings import TEST_TWITTER_USER, TEST_TWITTER_PASSWORD, TEST_FACEBOOK_USER, TEST_FACEBOOK_PASSWORD, TEST_DOMAIN, EMAIL_FILE_PATH, EMAIL_BACKEND
import unittest, string, random, sys, time, urlparse, project.settings

'''===================================================================================
home.tests.py: Testing for Home App Functionality:

Test classes: home.ModelTesting home.LoginTesting home.LoggingTesting home.UserProfileTesting 
home.EditUserProfileTesting home.FollowingTesting home.SocialAuthTesting
==================================================================================='''

'''===================================================================================
ModelTesting: Testing for EPM Models
==================================================================================='''
class ModelTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()
	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

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

		print ''
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

		print ''
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

		print ''
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
			pr = create_random_PetReport(user)
			
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
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_updatePetReport(self):
		print_testing_name("test_updatePetReport")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = create_random_PetReport(user)

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

		print ''
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
			pr = create_random_PetReport(user)

			PetReport.objects.get(proposed_by = user).delete()
			self.assertTrue(len(PetReport.objects.all()) == 0)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
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

		print ''
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

		print ''
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

		print ''
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
			pm.score = random.randint(0, 10000)
			pm.is_open = random.choice ([True, False])

			#Save it to the database.
			pm.save()
			pm_updated = PetMatch.objects.get(proposed_by = user.get_profile(), lost_pet = pr1, found_pet = pr2)

			#Now assert that the updated PetMatch matches the one we've just updated.
			self.assertEqual(pm, pm_updated)
			self.assertEqual(pm.score, pm_updated.score)
			self.assertEqual(pm.is_open, pm_updated.is_open)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
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

		print ''
		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == 0)
		performance_report(iteration_time)



'''===================================================================================
LoginTesting: Testing for EPM Logging In/Out
==================================================================================='''
class LoginTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_login_Users_successfully(self):
		print_testing_name("test_login_Users_successfully")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients) = create_test_view_setup()	

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Get the test objects.
			user, password = random.choice(users)
			client = random.choice(clients)

			print "[INFO]:%s logs onto %s and attempts to login..." % (user.username, client)

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
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)


'''===================================================================================
SocialAuthTesting: Testing for Social Authentication
==================================================================================='''
import urlparse
from selenium import webdriver
from django.test import TestCase
from project.settings import TEST_TWITTER_USER, TEST_TWITTER_PASSWORD
from project.settings import TEST_FACEBOOK_USER, TEST_FACEBOOK_PASSWORD
from project.settings import TEST_DOMAIN
from time import sleep

class SocialAuthTesting(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
        # pass

    def url(self, path):
        return urlparse.urljoin(TEST_DOMAIN, path)

    def test_twitter_authentication(self):
    	print "\n>>>> Testing 'test_twitter_authentication'"

        start_time = time.clock()

        # Assert the username and passward for the testing Twitter account are not none
        self.assertTrue(TEST_TWITTER_USER)
        self.assertTrue(TEST_TWITTER_PASSWORD)

        # Go to Twitter App Authorization page
        self.driver.get(self.url('/login/twitter/'))
        self.assertEqual("Twitter / Authorize an application", self.driver.title)
        print "  Redirecting to log in Twitter App Authorization page."

        # Log in Twitter using the testing user credential
        username_field = self.driver.find_element_by_id('username_or_email')
        username_field.send_keys(TEST_TWITTER_USER)
        password_field = self.driver.find_element_by_id('password')
        password_field.send_keys(TEST_TWITTER_PASSWORD)
 
        try:
        	# Try to log in
            password_field.submit()           
            sleep(5)
        
	        # If the testing user is not found in the user profile table,
	        # the user will be prompted to submit a username 
            try:
	        	assert "Social Account" in self.driver.title
	        	username_field = self.driver.find_element_by_id('username_id')
	        	# username = "twitter_test_user" + str(random.randrange(100, 999))
	        	username =  str(random.randrange(100, 999))
	        	username_field.send_keys(username)
	        	email_field = self.driver.find_element_by_id('email_id')
	         	email = "twitter_test_user@twitter.com"
	         	email_field.send_keys(email)
	         	# username_field.submit()	  
	         	self.driver.find_element_by_id("submit").click()
	         	# print "  Submitting a username '%s' for a created user profile account." % username
            except:
                pass
	        
	        # Assert the user logged in and has been redirected to the app home page 
	        # after successful authentication by Twitter 
            assert "EPM" in self.driver.title
            self.assertTrue(self.driver.find_element_by_id('logout'))
            print "  Successfully logging in EPM home page with Twitter authentication."
        except:
        	print "  Unable to authenticate the testing user with Twitter."

        end_time = time.clock()
        print '\n\tTotal Time: %s sec' % (end_time - start_time)
       

    def test_facebook_authentication(self):
    	print "\n>>>> Testing 'test_facebook_authentication'"

        start_time = time.clock()

        # Assert the username and passward for the testing Facebook account are not none
        self.assertTrue(TEST_FACEBOOK_USER)
        self.assertTrue(TEST_FACEBOOK_PASSWORD)

        # Go to Facebook App Authorization page
        self.driver.get(self.url('/login/facebook/'))
        self.assertEqual("Log In | Facebook", self.driver.title)
        print "  Redirecting to log in Facebook App Authorization page."

        # Log in Facebook using the testing user credential
        username_field = self.driver.find_element_by_id('email')
        username_field.send_keys(TEST_FACEBOOK_USER)
        password_field = self.driver.find_element_by_id('pass')
        password_field.send_keys(TEST_FACEBOOK_PASSWORD)

        try:
        	# Try to log in
            password_field.submit()           
            sleep(5)
             
            # If the testing user is not found in the user profile table,
            # the user will be prompted to submit a username
            try:
	        	assert "Social Account" in self.driver.title
	        	username_field = self.driver.find_element_by_id('username_id')
	        	# username = "facebook_test_user" + str(random.randrange(100, 999))
	        	username = str(random.randrange(100, 999))
	        	username_field.send_keys(username)
	         	username_field.submit()
	         	# print "  Submitting a username '%s' for a created user profile account." % username
            except:
                pass
  
            # Assert the user logged in and has been redirected to the app home page
            # after successful authentication by Facebook
            assert "EPM" in self.driver.title
            self.assertTrue(self.driver.find_element_by_id('logout'))
            print "  Successfully logging in EPM home page with Facebook authentication."

        except:
        	print "  Unable to authenticate the testing user with Facebook."
        	
        performance_report(end_time - start_time)

'''===================================================================================
UserProfileTesting: Testing for EPM User Profile Page
==================================================================================='''
class UserProfileTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_render_UserProfile_page(self):
		print_testing_name("test_render_UserProfile_page")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate accessing UserProfile pages.
		(users, clients) = create_test_view_setup()

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			user, password = random.choice(users)
			client = random.choice(clients)
			print_info_msg("%s logs onto %s to render the profile page..." % (user, client))

			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			response = client.get(URL_USERPROFILE + str(user.userprofile.id) + '/')

			self.assertTrue(response.status_code == 200)
			#We should have the base.html -> index.html -> userprofile.html
			self.assertTrue(len(response.templates) == 3)

			client.logout()
			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)


	def test_send_message_to_UserProfile(self):
		print_testing_name ("test_send_message_to_UserProfile")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords.
		(users, clients) = create_test_view_setup()

		#We assume that the subject's email address is formatted properly and is a real email address.
		#For testing purposes, we dump email messages to file and assert that their contents are correct.
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			user_one, password_one = random.choice(users)
			user_two, password_two = random.choice(users)
			userprofile_one = user_one.get_profile()
			userprofile_two = user_two.get_profile()
			client = random.choice(clients)

			if user_one.id == user_two.id:
				continue

			#Log onto the first user.
			loggedin = client.login(username = userprofile_one.user.username, password = password_one)
			self.assertTrue(loggedin == True)			
			print_info_msg ("%s logs onto %s to send a message to %s." % (userprofile_one.user.username, client, userprofile_two.user.username))

			# Go to the second user's profile page
			response = client.get(URL_USERPROFILE + str(userprofile_two.id) + "/")
			self.assertEquals(response.status_code, 200)
			#We should have the base.html -> index.html -> userprofile.html
			self.assertTrue(len(response.templates) == 3)

			#Email properties. We want the email body and subject so that we can check if they are what's actually written to the email.
			site = Site.objects.get(pk=1)
			message = generate_string(100)
			ctx = {"site":site, "message":message, "from_user":userprofile_one.user, "from_user_profile_URL": URL_USERPROFILE + str(userprofile_one.id)}
			email_body = render_to_string(TEXTFILE_EMAIL_USERPROFILE_MESSAGE, ctx)
			email_subject = "EmergencyPetMatcher: You have a new message from %s" % userprofile_one.user.username

			#Psuedo-send the email message.
			email = userprofile_one.send_email_message_to_UserProfile(userprofile_two, message, test_email=True)

			#Check for email properties.
			self.assertEquals (email ["subject"], email_subject)
			self.assertEquals (email ["body"], email_body)
			self.assertEquals (email ["from_username"], userprofile_one.user.username)
			self.assertEquals (email ["to_username"], userprofile_two.user.username)

			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)



'''===================================================================================
EditUserProfileTesting: Testing for EPM Edit User Profile Page
==================================================================================='''
class EditUserProfileTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()
	
	def test_editUserProfile_savePassword(self):
		print_testing_name("test_editUserProfile_savePassword")
		iteration_time = 0.00
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			(user,password) = create_random_User(i)
			client = Client (enforce_csrf_checks=False)
			user_i = user.id
			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the EditUserProfile page..." % (user, client)

			
			#Navigate to the EditUserProfile_form page
			response = client.get(URL_EDITUSERPROFILE)
			#Assert that the page was navigated to.
			self.assertEquals(response.status_code,200) 
			self.assertTrue(response.request ['PATH_INFO'] == URL_EDITUSERPROFILE)

			#Change the user's password
			new_password = generate_string (User._meta.get_field('password').max_length)
			confirm_password = generate_string (User._meta.get_field('password').max_length)

			#send the post request where the new_password & confirm_password do not match
			post =  {"action":"savePassword","old_password":password,"new_password":new_password,"confirm_password":confirm_password}
			
			response = client.post(URL_EDITUSERPROFILE, post,follow=True)
			user = User.objects.get(pk=user_i)
			#the password shouldn't have changed
			self.assertEquals(response.status_code,200) 
			self.assertFalse(user.check_password(new_password))

			#send the post request where the old password is not correct
			post =  {"action":"savePassword","old_password":new_password,"new_password":new_password,"confirm_password":confirm_password}
			
			response = client.post(URL_EDITUSERPROFILE, post,follow=True)
			user = User.objects.get(pk=user_i)
			#the password shouldn't have changed
			self.assertEquals(response.status_code,200) 
			self.assertFalse(user.check_password(new_password))

			#send the post request to change the password
			post =  {"action":"savePassword","old_password":password,"new_password":new_password,"confirm_password":new_password}
			
			response = client.post(URL_EDITUSERPROFILE, post,follow=True)
			user = User.objects.get(pk=user_i)
			#the password shouldn't have changed
			self.assertEquals(response.status_code,200) 
			self.assertTrue(user.check_password(new_password))

			print "[INFO]:Test test_editUserProfile_savePassword was successful for user %s" % (user)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		performance_report(iteration_time)


	def test_editUserProfile_saveProfile(self):
		print_testing_name("test_editUserProfile_saveProfile")
		iteration_time = 0.00
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			(user,password) = create_random_User(i)
			client = Client (enforce_csrf_checks=False)
			user_i = user.id
			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the EditUserProfile page..." % (user, client)

			#Edit the User's information and save it
			username = generate_string (User._meta.get_field('username').max_length)
			first_name = generate_string (User._meta.get_field('first_name').max_length)
			last_name = generate_string (User._meta.get_field('last_name').max_length)
			#email = user.email
			email = TEST_EMAIL 

			#Navigate to the EditUserProfile_form page
			response = client.get(URL_EDITUSERPROFILE)
			#Assert that the page was navigated to.
			self.assertEquals(response.status_code,200) 
			self.assertTrue(response.request ['PATH_INFO'] == URL_EDITUSERPROFILE)

			#the post data
			post =  {"action":"saveProfile","username":username,"first_name":first_name,"last_name":last_name,"email":email}
			#send the post request with the changes
			response = client.post(URL_EDITUSERPROFILE, post,follow=True)
			
			user = User.objects.get(pk=user_i)
			
			self.assertEquals(response.status_code,200) 
			#IF USERNAME EXISTS, NOTHING SHOULD CHANGE
			self.assertEquals(user.username,username)
			self.assertEquals(user.first_name,first_name)
			self.assertEquals(user.last_name,last_name)

			edituserprofile = EditUserProfile.objects.get(user=user)
			email_verification_url=URL_EMAIL_VERIFICATION_COMPLETE+edituserprofile.activation_key+"/"
			#navigate to verify the new email address
			response = client.get(email_verification_url)
			self.assertEquals(response.status_code,302)
			#assert that the user's email address has changed
			user = User.objects.get(pk=user_i)
			self.assertEquals(user.email,email)

			print "[INFO]:Test test_editUserProfile_saveProfile was successful for user %s" % (user)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		performance_report(iteration_time)
		

'''===================================================================================
FollowingTesting: Testing for EPM Following and Unfollowing functionalities
==================================================================================='''
class FollowingTesting (unittest.TestCase):

    # Get rid of all objects in the QuerySet.
    def setUp(self):
        User.objects.all().delete()
        UserProfile.objects.all().delete()

    # Get rid of all objects in the QuerySet.
    def tearDown(self):
        User.objects.all().delete()
        UserProfile.objects.all().delete()

    def test_following_and_unfollowing_a_UserProfile(self):
    	print_testing_name("test_following_and_unfollowing_a_UserProfile")
        iteration_time = 0.00

        # Need to setup clients, users, and their passwords in order to simula the following function.
        (users, clients) = create_test_view_setup()
        
        for i in range (NUMBER_OF_TESTS):
            start_time = time.clock()

            user_one, password_one = random.choice(users)
            user_two, password_two = random.choice(users)
            userprofile_one = user_one.get_profile()
            userprofile_two = user_two.get_profile()
            client = random.choice(clients)

            if user_one.id == user_two.id:
            	continue
           
            print "[INFO]: %s (id:%s) and %s (id:%s) have been created." % (userprofile_one, userprofile_one.id, userprofile_two, userprofile_two.id)

			#Log onto the first user.
            loggedin = client.login(username = userprofile_one.user.username, password = password_one)
            self.assertTrue(loggedin == True)			
            print "[INFO]: %s logs onto %s to follow %s." % (userprofile_one.user.username, client, userprofile_two.user.username)

            # Go to the second user's profile page
            response = client.get(URL_USERPROFILE + str(userprofile_two.id) + "/")
            self.assertEquals(response.status_code, 200)

            # ...................Testing Following Function.........................

            # Make the POST request Call for following the second user
            post = {"target_userprofile_id": userprofile_two.id}
            response = client.post(URL_FOLLOW, post, follow=True)

			# Make assertions
            self.assertEquals(response.status_code, 200)
            self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/UserProfile/'+ str(userprofile_two.id))
            self.assertEquals(response.redirect_chain[0][1], 302)
            self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(userprofile_two.id) + "/")

            # Assert that 
            # the second user is in the first user's following list, and 
            # the first user is in the second user's followers list
            self.assertTrue(userprofile_two in userprofile_one.following.all())
            self.assertTrue(userprofile_one in userprofile_two.followers.all())
            print "[INFO]: %s has followed %s." % (userprofile_one.user.username, userprofile_two.user.username)
 
            # ...................Testing Unfollowing Function.........................

            # Make the POST request Call for unfollowing the second user
            post = {"target_userprofile_id": userprofile_two.id}
            response = client.post(URL_UNFOLLOW, post, follow=True)

			# Make assertions
            self.assertEquals(response.status_code, 200)
            self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/UserProfile/'+ str(userprofile_two.id))
            self.assertEquals(response.redirect_chain[0][1], 302)
            self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(userprofile_two.id) + "/")
 
            # Assert that 
            # the second user is not in the first user's following list, and 
            # the first user is not in the second user's followers list
            self.assertTrue(not userprofile_two in userprofile_one.following.all())
            self.assertTrue(not userprofile_one in userprofile_two.followers.all())
            print "[INFO]: %s then unfollowed %s." % (userprofile_one, userprofile_two)

            # Logout the first user
            client.logout()
            output_update(i + 1)
            end_time = time.clock()
            iteration_time += (end_time - start_time)


        print ''
        self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
        self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
        performance_report(iteration_time)


'''===================================================================================
LoggingTesting: Testing for EPM Logging Activities
==================================================================================='''
class LoggingTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_create_activity_log(self):
		print_testing_name("test_create_activity_log")
		iteration_time = 0.00

		for i in range(NUMBER_OF_TESTS):
			start_time = time.clock()
			user = User.objects.create_user(username=generate_string(USER_USERNAME_LENGTH))
			userprofile = user.get_profile()
			userprofile.set_activity_log(is_test=True)

			#Now check: Does the userprofile's log file exist where it should?
			self.assertTrue(log_exists(userprofile) == True)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)				


	def test_delete_objects_and_check_log (self):
		print_testing_name("test_delete_objects_and_check_log")
		iteration_time = 0.00

		(users, clients, petreports, petmatches) = create_test_view_setup(create_following_lists=True, create_petreports=True, create_petmatches=True)
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
			print "[INFO]:%s logs onto %s..." % (user, client)

			#We expect the system not to throw errors but to catch them.
			activities = get_recent_activites_from_log(userprofile=user.userprofile)
			activities += get_bookmark_activities(userprofile=user.userprofile)
			print "[INFO]: %s has an activity feed list of size [%d]" % (user, len(activities))
			self.assertTrue(log_exists(user.userprofile))

			#Now, delete the user.
			user.delete()
			self.assertFalse(log_exists(user.userprofile))

			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)


	def test_log_account_creations(self):
		print_testing_name("test_log_account_creations")
		iteration_time = 0.00

		for i in range(NUMBER_OF_TESTS):
			start_time = time.clock()
			(user, password) = create_random_User(i)
			user_log_filename = TEST_ACTIVITY_LOG_DIRECTORY + str(user.get_profile().id) + ".log"

			with open(user_log_filename, 'r') as logger:

				lines = list(iter(logger.readlines()))
				print lines
				self.assertTrue(activity_has_been_logged(ACTIVITY_ACCOUNT_CREATED, user.get_profile()) == True)
				self.assertEquals(len(lines), 1)

			logger.close()
			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)		


	def test_log_submit_PetReport(self):
		print_testing_name("test_log_submit_PetReport")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients) = create_test_view_setup()

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
			self.assertTrue(activity_has_been_logged(ACTIVITY_PETREPORT_SUBMITTED, user.get_profile(), petreport=petreport) == True)	

			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == 2*NUMBER_OF_TESTS) 
		performance_report(iteration_time)


	def test_log_propose_PetMatch (self):
		print_testing_name("test_log_propose_PetMatch")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the matching interface..." % (user, client)			

			#Go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)
			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print "[INFO]: Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue

			self.assertEquals(response.status_code, 200)
			print "[INFO]:%s has successfully requested page '%s'..." % (user, matching_url) 
			candidate_petreport = random.choice(filtered_pet_reports) 

			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print "[INFO]:%s has successfully requested page '%s'..." % (user, propose_match_url) 

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

			#Either the User upvoting an already existing PetMatch...
			if match.UserProfile_has_voted(user.get_profile()) == UPVOTE:
				print "[INFO]:A PetMatch already exists with these two PetReports, and so %s has up-voted this match!" % (user)
				self.assertTrue(activity_has_been_logged(ACTIVITY_PETMATCH_UPVOTE, user.get_profile(), petmatch=match) == True)

			#...Or the User successfully proposed a NEW PetMatch.
			else:
				print "[INFO]:%s has successfully POSTED a new match!" % (user)
				self.assertTrue(activity_has_been_logged(ACTIVITY_PETMATCH_PROPOSED, user.get_profile(), petmatch=match) == True)					
	
			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)

	def test_log_following_UserProfile(self):
		print_testing_name("test_log_following_UserProfile")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients) = create_test_view_setup()

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
			print "[INFO]:%s logs onto %s to follow %s." % (userprofile_one.user.username, client, userprofile_two.user.username)

			# Go to the second user's profile page
			response = client.get(URL_USERPROFILE + str(userprofile_two.id) + "/")
			self.assertEquals(response.status_code, 200)

			# Make the POST request Call for following the second user
			post = {'target_userprofile_id': userprofile_two.id}
			response = client.post(URL_FOLLOW, post, follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()						

			# Check if the activity for following a UserProfile appears in this userprofile_one's log.
			self.assertTrue(activity_has_been_logged(ACTIVITY_FOLLOWING, userprofile=userprofile_one, userprofile2=userprofile_two) == True)		
			print "[OK]:%s has followed %s" % (userprofile_one.user.username, userprofile_two.user.username)

			# Check if the activity for following a UserProfile appears in this userprofile_two's log.
			self.assertTrue(activity_has_been_logged(ACTIVITY_FOLLOWER, userprofile=userprofile_two, userprofile2=userprofile_one) == True)				
			print "[OK]:%s has been followed by %s" % (userprofile_two.user.username, userprofile_one.user.username)
	
			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)


	def test_log_unfollowing_UserProfile(self):
		print_testing_name("test_log_unfollowing_UserProfile")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients) = create_test_view_setup()

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
			print "[INFO]:%s logs onto %s to follow %s." % (userprofile_one.user.username, client, userprofile_two.user.username)			

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
			self.assertTrue(activity_has_been_logged(ACTIVITY_UNFOLLOWING, userprofile=userprofile_one, userprofile2=userprofile_two) == True)			
			print "[OK]:%s has unfollowed %s" % (userprofile_one.user.username, userprofile_two.user.username)
				
			# Check if the activity for unfollowing a UserProfile appears in this userprofile_two's log.
			self.assertTrue(activity_has_been_logged(ACTIVITY_UNFOLLOWER, userprofile=userprofile_two, userprofile2=userprofile_one) == True)			
			print "[OK]:%s has been unfollowed by %s" % (userprofile_two.user.username, userprofile_one.user.username)
				
			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)


	def test_log_add_PetReport_bookmark(self):
		print_testing_name("test_log_add_PetReport_bookmark")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)
			print "[INFO]: A user %s and a pet report %s have been created." % (user.userprofile, petreport)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]: %s logs onto %s to enter the prdp interface to add a bookmark." % (user, client)			

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
			response = client.post(add_bookmark_url, post, follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()	
			new_bookmarks_count = user.get_profile().bookmarks_related.count()
			
			#Make assertions
			if not previously_bookmarked:
				self.assertEquals(old_bookmarks_count, (new_bookmarks_count-1))

			# Check if the activity for adding a PetReport bookmark appears in this user's log.
			print "[INFO]: %s has added a bookmark for %s." % (user, petreport)
			self.assertTrue(activity_has_been_logged(ACTIVITY_PETREPORT_ADD_BOOKMARK, userprofile=user.get_profile(), petreport=petreport) == True)

			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)


	def test_log_remove_PetReport_bookmark(self):
		print_testing_name("test_log_remove_PetReport_bookmark")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)
			print "[INFO]: A user %s and a pet report %s have been created." % (user.userprofile, petreport)

			# Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the prdp interface to remove a bookmark." % (user, client)			

			# Go to the PRDP (Pet Report Detailed Page) interface
			response = client.get(URL_PRDP + str(petreport.id) + "/")
			self.assertEquals(response.status_code, 200)

			# Add a bookmark
			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)	
			self.assertEquals(response.status_code, 200)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			# Remove the bookmark
			remove_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Remove Bookmark"}
			response = client.post(remove_bookmark_url, post, follow=True)
			self.assertEquals(response.status_code, 200)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()
			client.logout()	

			#Make assertions
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))

			# Check if the activity for adding a PetReport bookmark appears in this user's log.
			print "[INFO]: %s has removed a bookmark for %s." % (user, petreport)
			self.assertTrue(activity_has_been_logged(ACTIVITY_PETREPORT_ADD_BOOKMARK, userprofile=user.get_profile(), petreport=petreport) == True)				

			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)


	def test_get_activities_json(self):
		print_testing_name("test_get_activities_json")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the matching interface..." % (user, client)	

			#Request the get_activities_json view function()
			response = client.get(URL_GET_ACTIVITIES, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			client.logout()	

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], URL_GET_ACTIVITIES)

			#But now, let's test to get and assert those actual activities
			activities = []
			random_activity_range = random.randrange(0, len(UserProfile.objects.all()))
			for following in user.get_profile().following.all().order_by("?")[:random_activity_range]:
				log = get_recent_activites_from_log(following)
				if log != None:
					activities.append(log)

			num_following = len(user.get_profile().following.all())
			num_activities = len(activities)
			print "[INFO]: %s has %d followers and got an activity feed list of size %d when ACTIVITY_FEED_LENGTH = %d" % (user, num_following, num_activities, random_activity_range)

			#Bounds checking
			self.assertTrue(num_activities >= 0 and num_activities <= random_activity_range)

			if random_activity_range < num_following:
				self.assertTrue(num_activities == random_activity_range)
			else:
				self.assertTrue(num_activities <= num_following)

			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)	


	def test_get_activities_json_for_anonymous_user(self):
		print_testing_name("test_get_activities_json_for_anonymous_user")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients) = create_test_view_setup()

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
			max_num_activities = ACTIVITY_FEED_LENGTH
			for userprof in UserProfile.objects.order_by("?").filter(user__is_active=True)[:max_num_activities]:
				activities += get_recent_activites_from_log(userprofile=userprof, num_activities=1)			
			num_activities = len(activities)
			print "=======[INFO]: The anonymous user got an activity feed list of size %d when the maximum length = %d" % (num_activities, max_num_activities)

			#Bounds checking
			self.assertTrue(num_activities >= 0 and num_activities <= max_num_activities)

			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)	


	def test_get_activities_json_for_authenticated_user(self):
		print_testing_name("test_get_activities_json_for_authenticated_user")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
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

			# Make the POST request Call for user to add a bookmark for a random petreport
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Bookmark this Pet"}
			response = client.post(URL_BOOKMARK_PETREPORT, post, follow=True)
			self.assertEquals(response.status_code, 200)

			#Summing up the minimum value of user's activity feeds
			min_num_activities = len(user.get_profile().followers.all()) + len(user.get_profile().following.all())

			#Request the get_activities_json view function()
			response = client.get(URL_GET_ACTIVITIES, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			client.logout()	

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], URL_GET_ACTIVITIES)

			#But now, let's test to get and assert those actual activities
			activities = []

			# Get all activities from this UserProfile's log file that show who has followed this UserProfile 
			activities += get_recent_activites_from_log(userprofile=user.get_profile(), current_userprofile=user.get_profile(), since_date=user.get_profile().last_logout, activity=ACTIVITY_FOLLOWER)

			# Get all activities that associated to the PetReports I bookmarked
			activities += get_bookmark_activities(userprofile=user.get_profile(), since_date=user.get_profile().last_logout)

            # Get all activities that are associated with the UserProfiles I follow
			for following in user.get_profile().following.all():
				activities += get_recent_activites_from_log(userprofile=following, current_userprofile=user.get_profile(), since_date=user.get_profile().last_logout)

			num_following = len(user.get_profile().following.all())
			num_activities = len(activities)
			print "[INFO]: %s has %d followers and got an activity feed list of size %d when the minimum length = %d" % (user, num_following, num_activities, min_num_activities)

			#Bounds checking
			# self.assertTrue(num_activities >= min_num_activities)

			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)	

'''===================================================================================
ReputationTesting: Testing for EPM User Reputation Points
==================================================================================='''
class ReputationTesting(unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_reputation_points_for_upvoting_PetMatch (self):
		print_testing_name("test_reputation_points_for_upvoting_PetMatch")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users) 
			old_reputation = user.userprofile.reputation
			client = random.choice(clients)
			petmatch = random.choice(petmatches)

			#checking reputation points for the user who proposed a petmatch
			pm_proposed_by_user = PetMatch.objects.get(pk=petmatch.id).proposed_by
			p_old_reputation = pm_proposed_by_user.reputation
			voted = False

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the PMDP..." % (user, client)

			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			response = client.get(pmdp_url)
			
			print "[INFO]: Reputation points for %s BEFORE upvoting: %s" % (user, old_reputation)
			print "[INFO]: Reputation points for %s (who proposed this PetMatch) BEFORE upvoting: %s" %(pm_proposed_by_user, p_old_reputation)
			print "[INFO] Voted or not for this petmatch before: %s" % petmatch.UserProfile_has_voted(user.get_profile())
			
			# check if the user has voted before or not and set the 'voted' flag accordingly
			if petmatch.UserProfile_has_voted(user.get_profile()) is False:
				voted = False
				print "[INFO]: *** User has NEVER voted for this petmatch ***"
			else:
				voted = petmatch.UserProfile_has_voted(user.get_profile())
				print "[INFO]: *** User has Voted for this petmatch before ***"

			vote_url = URL_VOTE_MATCH
			post =  {"vote":"upvote", "match_id":petmatch.id, "user_id":user.id}
			response = client.post(vote_url, post, follow=True)

			# Reset user with a new fresh copy from the DB.
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)

			print "[INFO]: Reputation points for %s AFTER upvoting: %s" %(user, user.get_profile().reputation)
			pm_proposed_by_user = PetMatch.objects.get(pk=petmatch.id).proposed_by
			print "[INFO]: Reputation points for %s (who proposed this PetMatch) AFTER upvoting: %s" %(pm_proposed_by_user, pm_proposed_by_user.reputation)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], vote_url)
			self.assertTrue(petmatch.UserProfile_has_voted(user.get_profile()) == UPVOTE)
			self.assertEquals(petmatch.up_votes.get(pk=user.id), user.get_profile())

			if (voted == False) and (user.get_profile().id != pm_proposed_by_user.id):
				self.assertEquals(user.get_profile().reputation, old_reputation + REWARD_PETMATCH_VOTE)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation + REWARD_USER_PROPOSED_PETMATCH_VOTE)
			
			elif (voted == UPVOTE) and (user.get_profile().id != pm_proposed_by_user.id):
				self.assertEquals(user.get_profile().reputation, old_reputation)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation)

			elif (voted == DOWNVOTE) and (user.get_profile().id != pm_proposed_by_user.id):
				self.assertEquals(user.get_profile().reputation, old_reputation)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation + REWARD_USER_PROPOSED_PETMATCH_VOTE)
			
			elif (voted == False) and (user.get_profile().id == pm_proposed_by_user.id):
				self.assertEquals(user.get_profile().reputation, old_reputation + REWARD_PETMATCH_VOTE + REWARD_USER_PROPOSED_PETMATCH_VOTE)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation + REWARD_PETMATCH_VOTE + REWARD_USER_PROPOSED_PETMATCH_VOTE)
			else:
				print "[ERROR]: Unexpected case..."

			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)


	def test_reputation_points_for_downvoting_PetMatch (self):
		print_testing_name("test_reputation_points_for_downvoting_PetMatch")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			old_reputation = user.userprofile.reputation
			client = random.choice(clients)
			petmatch = random.choice(petmatches)
			
			#checking reputation points for the user who proposed a petmatch
			pm_proposed_by_user = PetMatch.objects.get(pk=petmatch.id).proposed_by
			p_old_reputation = pm_proposed_by_user.reputation
			voted = False

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the PMDP..." % (user, client)

			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			print pmdp_url
			response = client.get(pmdp_url)
			
			print "[INFO]: Reputation points BEFORE downvoting: %s" % (old_reputation)
			print "[INFO]: Voted or not for this petmatch before: %s" % petmatch.UserProfile_has_voted(user.get_profile())
			print "[INFO]: Reputation points for %s (who proposed this PetMatch) BEFORE downvoting: %s" % (pm_proposed_by_user, p_old_reputation)
			
			# check if the user has voted before or not and set the 'voted' flag accordingly
			if petmatch.UserProfile_has_voted(user.get_profile()) is False:
				voted = False
				print "[INFO]: *** User has NEVER voted for this petmatch ***"
			elif petmatch.UserProfile_has_voted(user.get_profile()) is not False:
				voted = petmatch.UserProfile_has_voted(user.get_profile())
				print "[INFO]: *** User has Voted for this petmatch before ***"
			else:
				print "[ERROR]:Something is wrong!"

			vote_url = URL_VOTE_MATCH
			post =  {"vote":"downvote", "match_id":petmatch.id, "user_id":user.id}
			response = client.post(vote_url, post, follow=True)

			# Reset user with a new fresh copy from the DB
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)

			print "[INFO]: Reputation points AFTER downvoting: %s" %(user.get_profile().reputation)
			pm_proposed_by_user = PetMatch.objects.get(pk=petmatch.id).proposed_by
			print "[INFO]: Reputation points for %s (who proposed this PetMatch) AFTER downvoting: %s" %(pm_proposed_by_user, pm_proposed_by_user.reputation)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], vote_url)
			self.assertTrue(petmatch.UserProfile_has_voted(user.get_profile()) == DOWNVOTE)
			self.assertEquals(petmatch.down_votes.get(pk = user.id), user.get_profile())
			
			if (voted == False) and (user.get_profile().id != pm_proposed_by_user.id):
				self.assertEquals(user.get_profile().reputation, old_reputation + REWARD_PETMATCH_VOTE)
			
			elif (voted == DOWNVOTE) and (user.get_profile().id != pm_proposed_by_user.id):
				self.assertEquals(user.get_profile().reputation, old_reputation)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation)
			
			elif (voted == UPVOTE) and (user.get_profile().id != pm_proposed_by_user.id):
				self.assertEquals(user.get_profile().reputation, old_reputation)
			
			elif (not voted) and (user.get_profile().id == pm_proposed_by_user.id):
				self.assertEquals(user.get_profile().reputation, old_reputation + REWARD_PETMATCH_VOTE)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation + REWARD_PETMATCH_VOTE)
			else:
				print "[ERROR]:Assert FAILED! Something is wrong!"

			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)


	def test_reputation_points_for_submitting_PetReport(self):
		print_testing_name("test_reputation_points_for_submitting_PetReport")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients) = create_test_view_setup(create_petreports=False)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			old_reputation = user.userprofile.reputation
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
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)

			print "[INFO]: Reputation points BEFORE submitting a PetReport: %s" %(old_reputation)

			#Make the POST request Call
			response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)

			# Reset user with a new fresh copy from the DB
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)
			print "[INFO]: Reputation points AFTER submitting a PetReport: %s" %(user.get_profile().reputation)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertTrue(len(response.redirect_chain) == 1) 
			# self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)
			self.assertTrue(len(PetReport.objects.all()) == 2*i + 2)
			self.assertNotEquals(user.get_profile().reputation, old_reputation)
			self.assertEquals(user.get_profile().reputation, old_reputation + REWARD_PETREPORT_SUBMIT)
			client.logout()

			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == 2*NUMBER_OF_TESTS) 
		performance_report(iteration_time)


	def test_reputation_points_for_proposing_PetMatch(self):
		print_testing_name("test_reputation_points_for_proposing_PetMatch")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports) = create_test_view_setup(create_petreports=True)
		num_petmatches = 0

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			old_reputation = user.userprofile.reputation
			client = random.choice(clients)
			petreport = random.choice(petreports)

			# PetMatch status flag to check if the user gets proposing points for proposing a new petmatch
			# or for voting points when proposing a duplicate petmatch but never voted it before
			pm_status = ACTIVITY_PETMATCH_PROPOSED

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the matching interface..." % (user, client)			

			#Go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print "[INFO]:Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue

			self.assertEquals(response.status_code, 200)
			print "[INFO]:%s has successfully requested page '%s'..." % (user, matching_url) 
			candidate_petreport = random.choice(filtered_pet_reports) 

			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print "[INFO]:%s has successfully requested page '%s'..." % (user, propose_match_url) 
			print "[INFO]: Reputation points BEFORE proposing a PetMatch: %s" %(old_reputation)

			#Grab the PetMatch that is either a new one, has been posted in the past or has been posted by this User, and set the pm_status flag accordingly based on the activities.
			match = PetMatch.get_PetMatch(petreport, candidate_petreport)
			if match is not None:
				if match.UserProfile_has_voted(user.get_profile()) is not False:
					print "[OK]:A duplicate PetMatch, and %s has VOTED this match before!" % (user)
					print "[INFO]: User will get no points."
					pm_status = None
				elif match.UserProfile_has_voted(user.get_profile()) is False:
					print "[OK]: A duplicate PetMatch, and %s has NEVER voted this match before!" % (user)
					print "[INFO]: User will get voting points."
					pm_status = ACTIVITY_PETMATCH_UPVOTE
				else:
					print "[ERROR]:Something went wrong with checking the UserProfile_has_voted function!"
			elif match is None:
				print "[OK]:This will be a new PetMatch."
				print "[INFO]: User will get proposing points."
				pm_status = ACTIVITY_PETMATCH_PROPOSED
			else:
				print "[ERROR]:Something went wrong while checking of the 'match exists or not!"

			#Make the POST request Call		
			description = generate_lipsum_paragraph(500)
			post = {'description': description}
			response = client.post(propose_match_url, post, follow=True)
			client.logout()

			# Reset user with a new fresh copy from the DB
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)
			print "[INFO]: Reputation points AFTER proposing a PetMatch: %s" %(user.get_profile().reputation)

			#Grab the PetMatch, again, that has either been posted in the past or has been posted by this User.
			match = PetMatch.get_PetMatch(petreport, candidate_petreport)
			if match.UserProfile_has_voted(user.get_profile()) is not False:
				print "[OK]:A PetMatch already exists with these two PetReports, and so %s has up-voted this match!" % (user)
			else:
				print "[OK]: has successfully POSTED a new match!" % (user)				
				num_petmatches += 1

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(len(response.redirect_chain), 1)
			# self.assertEquals(response.redirect_chain[0][0], 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertEquals(response.request ['PATH_INFO'], URL_HOME)	
			if pm_status == ACTIVITY_PETMATCH_PROPOSED:
				self.assertEquals(user.get_profile().reputation, old_reputation+REWARD_PETMATCH_PROPOSE)
			elif pm_status == ACTIVITY_PETMATCH_UPVOTE:
				self.assertEquals(user.get_profile().reputation, old_reputation+REWARD_PETMATCH_VOTE)
			elif pm_status == None:
				self.assertEquals(user.get_profile().reputation, old_reputation)
			else:
				print "[ERROR]:Assert Failed! Something went wrong with reputation points!"			

			#Some checks for the PetMatch objects stored
			self.assertTrue(len(PetMatch.objects.all()) == num_petmatches or len(PetMatch.objects.all()) <= i)
			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		performance_report(iteration_time)


	def test_reputation_points_for_a_UserProfile_being_followed_and_unfollowed(self):
	    print_testing_name("test_reputation_points_for_a_UserProfile_being_followed_and_unfollowed")
	    iteration_time = 0.00

	    # Need to setup clients, users, and their passwords in order to simula the following function.
	    (users, clients) = create_test_view_setup(create_petreports=False, create_petmatches=False)
	        
	    for i in range (NUMBER_OF_TESTS):
	        start_time = time.clock()

	        # objects
	        user_one, password_one = random.choice(users)
	        user_two, password_two = random.choice(users)
	        userprofile_one = user_one.get_profile()
	        userprofile_two = user_two.get_profile()
	        old_reputation = userprofile_two.reputation
	        client = random.choice(clients)

	        if user_one.id == user_two.id:
	        	continue

	        print "\n%s ............................................................." % i
	        print "[INFO]: %s (id:%s) and %s (id:%s) have been created." % (userprofile_one, userprofile_one.id, userprofile_two, userprofile_two.id)

			#Log onto the first user.
	        loggedin = client.login(username = userprofile_one.user.username, password = password_one)
	        self.assertTrue(loggedin == True)			
	        print "[INFO]: %s logs onto %s to follow %s." % (userprofile_one.user.username, client, userprofile_two.user.username)

	        # Go to the second user's profile page
	        response = client.get(URL_USERPROFILE + str(userprofile_two.id) + "/")
	        self.assertEquals(response.status_code, 200)

	        print "[INFO]: Reputation points for %s BEFORE being followed: %s" %(userprofile_two, old_reputation)

	        # ...................Testing Following Function.........................

	        # Make the POST request Call for following the second user
	        post = {"target_userprofile_id": userprofile_two.id}
	        response = client.post(URL_FOLLOW, post, follow=True)

	        # Reset userprofile_two with a new fresh copy from the db
	        userprofile_two = UserProfile.objects.get(pk=user_two.id)
	        print "[INFO]: Reputation points for %s AFTER being followed: %s" %(userprofile_two, userprofile_two.reputation)

			# Make assertions
	        self.assertEquals(response.status_code, 200)
	        self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/UserProfile/'+ str(userprofile_two.id))
	        self.assertEquals(response.redirect_chain[0][1], 302)
	        self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(userprofile_two.id) + "/")
	        self.assertEquals(userprofile_two.reputation, old_reputation+REWARD_USER_FOLLOWED)

	        # Assert that 
	        # the second user is in the first user's following list, and 
	        # the first user is in the second user's followers list
	        self.assertTrue(userprofile_two in userprofile_one.following.all())
	        self.assertTrue(userprofile_one in userprofile_two.followers.all())
	        print "[INFO]: %s has followed %s." % (userprofile_one.user.username, userprofile_two.user.username)

	        # ...................Testing Unfollowing Function.........................

	        # reset old_reputation with a new fresh copy from the db
	        old_reputation = userprofile_two.reputation
	        print "[INFO]: Reputation points for %s BEFORE being unfollowed: %s" %(userprofile_two, old_reputation)

	        # Make the POST request Call for unfollowing the second user
	        post = {"target_userprofile_id": userprofile_two.id}
	        response = client.post(URL_UNFOLLOW, post, follow=True)

	        # reset userprofile_two with a new fresh copy from the db
	        userprofile_two = UserProfile.objects.get(pk=user_two.id)
	        print "[INFO]: Reputation points for %s AFTER being unfollowed: %s" %(userprofile_two, userprofile_two.reputation)

			# Make assertions
	        self.assertEquals(response.status_code, 200)
	        self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/UserProfile/'+ str(userprofile_two.id))
	        self.assertEquals(response.redirect_chain[0][1], 302)
	        self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(userprofile_two.id) + "/")

	        # Assert that 
	        # the second user is not in the first user's following list, and 
	        # the first user is not in the second user's followers list
	        self.assertTrue(not userprofile_two in userprofile_one.following.all())
	        self.assertTrue(not userprofile_one in userprofile_two.followers.all())
	        print "[INFO]: %s then unfollowed %s." % (userprofile_one, userprofile_two)

	        self.assertEquals(userprofile_two.reputation, old_reputation-REWARD_USER_FOLLOWED)

	        # Logout the first user
	        client.logout()

	        end_time = time.clock()
	        iteration_time += (end_time - start_time)


	        print ''
	        self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
	        self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
	        performance_report(iteration_time)


	def test_reputation_points_for_adding_and_removing_PetReport_bookmark(self):
		print_testing_name("test_reputation_points_for_adding_and_removing_PetReport_bookmark")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate bookmarking of PetReport objects.
		(users, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			old_reputation = user.userprofile.reputation
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the PRDP..." % (user, client)

			#navigate to the prdp
			prdp_url = URL_PRDP + str(petreport.id) + "/"
			print prdp_url
			response = client.get(prdp_url)

			# ...................Testing Adding a Bookmark.........................
			print "[INFO]: Reputation points BEFORE bookmarking a PetReport: %s" %(old_reputation)

			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			# reset user with a new fresh copy from the db
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)

			print "[INFO]: Reputation points AFTER bookmarking a PetReport: %s" %(user.get_profile().reputation)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], add_bookmark_url)
			self.assertEquals(user.get_profile().reputation, old_reputation+REWARD_PETREPORT_BOOKMARK)


			# ...................Testing Removing a Bookmark.........................
			old_reputation = user.get_profile().reputation
			print "[INFO]: Reputation points BEFORE unbookmarking a PetReport: %s" %(old_reputation)

			remove_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Remove Bookmark"}
			response = client.post(remove_bookmark_url, post, follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()

			# Reset user with a new fresh copy from the db
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)

			print "[INFO]: Reputation points AFTER unbookmarking a PetReport: %s" %(user.get_profile().reputation)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], remove_bookmark_url)
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))
			self.assertEquals(user.get_profile().reputation, old_reputation-REWARD_PETREPORT_BOOKMARK)


			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''

		performance_report(iteration_time)

	def test_reputation_points_for_PetMatch_verification(self):
		print_testing_name = ("test_reputation_points_for_PetMatch_verification")
		iteration_time = 0.00
		# setup clients, users and their passwords
		(users, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			# objects
			client = random.choice(clients)
			petmatch = random.choice(petmatches)
			proposers = [petmatch.lost_pet.proposed_by.user, petmatch.found_pet.proposed_by.user]
			lost_pet_proposer_index = [user[0] for user in users].index(proposers[0])
			found_pet_proposer_index = [user[0] for user in users].index(proposers[1])

			if petmatch.PetMatch_has_reached_threshold() == False:
				continue

			# Looking for other users and their passwords in the users list
			for (user, password) in [users[lost_pet_proposer_index], users[found_pet_proposer_index]]:
				petmatch = PetMatch.objects.get(pk=petmatch.id)
				petmatch_owner = petmatch.proposed_by
				lost_pet_contact = petmatch.lost_pet.proposed_by
				found_pet_contact = petmatch.found_pet.proposed_by
				# reputation: [0]petmatch_owner, [1]lost_pet_contact, [2]found_pet_contact
				reputation = [petmatch_owner.reputation, lost_pet_contact.reputation, found_pet_contact.reputation]
				
				print 20*"=" + "*BEGIN*" + 20*"="

				# log in first
				loggedin = client.login(username = user.username, password = password)
				self.assertTrue(loggedin == True)
				print "[INFO]: %s logs onto %s to enter the verification page..." % (user, client)

				print '[INFO]: petmatch users: %s, %s ' % (str(petmatch.lost_pet.proposed_by.user), str(petmatch.found_pet.proposed_by.user))

				verification_page_url = URL_VERIFY_PETMATCH + str(petmatch.id) + "/"
				print verification_page_url

				response = client.get(verification_page_url)
				userprofile = user.get_profile()
				self.assertEquals(response.status_code, 200)

				print "[INFO]:PetMatch owner (%s) reputation BEFORE: %s " % (petmatch_owner.user, reputation[0])
				print "[INFO]:Lost pet contact (%s) reputation BEFORE: %s " % (lost_pet_contact.user, reputation[1])
				print "[INFO]:Found pet contact (%s) reputation BEFORE: %s " % (found_pet_contact.user, reputation[2])

				old_verification_vote = int(petmatch.verification_votes[0])
				old_verification_votes = str(petmatch.verification_votes)
				print "[INFO]: OLD verification vote: %s" %old_verification_vote
				print "[INFO]: OLD verification votes: %s" %old_verification_votes

				print "----UPVOTERS----"
				for upvoters in petmatch.up_votes.all():
					print "%s reputation BEFORE: %s" %(upvoters.user, upvoters.reputation)
				print "----------------"
				
				message = random.choice(['yes', 'no'])
				# message = 'yes'
				post = {'message':message}
				response = client.post(verification_page_url, post, follow=True)
				self.assertEquals(response.status_code, 200)
				
				petmatch = PetMatch.objects.get(pk=petmatch.id)
				new_verification_vote = int(petmatch.verification_votes[0])
				new_verification_votes = str(petmatch.verification_votes)
				petmatch_owner = petmatch.proposed_by
				lost_pet_contact = petmatch.lost_pet.proposed_by
				found_pet_contact = petmatch.found_pet.proposed_by
				print "[INFO]: NEW verification vote: %s" %new_verification_vote
				print "[INFO]: NEW verification votes: %s" %new_verification_votes
				print "[INFO] Is successful: %s" %petmatch.is_successful
				print "[INFO]:PetMatch owner (%s) reputation AFTER: %s " % (petmatch_owner.user, petmatch_owner.reputation)
				print "[INFO]:Lost pet contact (%s) reputation AFTER: %s " % (lost_pet_contact.user, lost_pet_contact.reputation)
				print "[INFO]:Found pet contact (%s) reputation AFTER: %s " % (found_pet_contact.user, found_pet_contact.reputation)
				
				print "----UPVOTERS----"
				for upvoters in petmatch.up_votes.all():
					print "%s reputation AFTER: %s" %(upvoters.user, upvoters.reputation)
				print "----------------"

				sent_vote = 0
				if old_verification_vote == 0:
					if message == 'yes':
						sent_vote = 1
					elif message == 'no':
						sent_vote = 2
					else:
						sent_vote = 0
					self.assertEquals(new_verification_vote, sent_vote)
				else:
					self.assertEquals(old_verification_vote, new_verification_vote)

				# assert reputation points for the possible cases
				if old_verification_votes != new_verification_votes:
					# successful petmatch verification
					if new_verification_votes == '11':

						if petmatch_owner.id == lost_pet_contact.id:
							if petmatch_owner in petmatch.up_votes.all() or lost_pet_contact in petmatch.up_votes.all():
								self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
								self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							if found_pet_contact in petmatch.up_votes.all():
								self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							else:
								self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)
								self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)
								self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)

						elif petmatch_owner.id == found_pet_contact.id:
							if petmatch_owner in petmatch.up_votes.all() or found_pet_contact in petmatch.up_votes.all():
								self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
								self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							if lost_pet_contact in petmatch.up_votes.all():
								self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							else:
								self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)
								self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)
								self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)

						elif (petmatch_owner in petmatch.up_votes.all()) and (lost_pet_contact in petmatch.up_votes.all()) and (found_pet_contact in petmatch.up_votes.all()):
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)

						elif (petmatch_owner in petmatch.up_votes.all()) and (lost_pet_contact in petmatch.up_votes.all()):
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)

						elif (petmatch_owner in petmatch.up_votes.all()) and (found_pet_contact in petmatch.up_votes.all()):
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)
							self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)

						elif (lost_pet_contact in petmatch.up_votes.all()) and (found_pet_contact in petmatch.up_votes.all()):
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL)
							self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)

						elif petmatch_owner in petmatch.up_votes.all():
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)
							self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)

						elif lost_pet_contact in petmatch.up_votes.all():
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL)
							self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)
							self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)

						elif found_pet_contact in petmatch.up_votes.all():
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL)
							self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)
							self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL+REWARD_PETMATCH_UPVOTE_SUCCESSFUL)

						else:
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL)
							self.assertEquals(lost_pet_contact.reputation, reputation[1]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)
							self.assertEquals(found_pet_contact.reputation, reputation[2]+REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL)

					# failure petmatch verification
					else:
						if new_verification_votes == '22' or new_verification_votes == '12' or new_verification_votes == '21':
							self.assertEquals(petmatch_owner.reputation, reputation[0]+REWARD_USER_PROPOSED_PETMATCH_FAILURE)
				else:
					self.assertEquals(petmatch_owner.reputation, reputation[0])
					self.assertEquals(lost_pet_contact.reputation, reputation[1])
					self.assertEquals(found_pet_contact.reputation, reputation[2])
				
				
				print 21*"=" + "*END*" + 21*"="

			output_update(i+1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

'''===================================================================================
HomePageTesting: Testing for the EPM Home Page
==================================================================================='''
class HomePageTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()	

	def test_homepage_newlyadded(self):
		print_testing_name("test_homepage_newlyadded")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			response = client.get(URL_HOME)
			self.assertEquals(response.status_code,200)
			#Testing if the list of pets in the home page are ordered in reverse chronological fashion
			# print response.context
			pet_reports_list = response.context['pet_reports_list']
			pet_reports = PetReport.objects.filter(closed = False).order_by("id").reverse()
			self.assertEquals(str(pet_reports_list.object_list.all()),str(pet_reports))

