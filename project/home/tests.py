from django.contrib.auth import authenticate
from django.test.client import Client
from utils import *
from constants import *
from home.models import *
from logging import *
from time import sleep
from selenium import webdriver
from project.settings import TEST_TWITTER_USER, TEST_TWITTER_PASSWORD
from project.settings import TEST_FACEBOOK_USER, TEST_FACEBOOK_PASSWORD
from project.settings import TEST_DOMAIN
import unittest, string, random, sys, time, urlparse

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
		(users, passwords, clients) = create_test_view_setup(create_petreports=False)	

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			user = users [user_i]
			client = clients [client_i]

			print "[INFO]:%s logs onto %s and attempts to login..." % (user, client)

			#Go to the Login Page
			response = client.get(URL_LOGIN)
			next = response.context ['next']
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request ['PATH_INFO'] == URL_LOGIN)
			self.assertTrue(next == URL_HOME)

			#Submit Login information
			response = client.post (URL_LOGIN, 
				{'username':users [user_i].username, 'password': passwords [user_i], 'next': next}, follow=True)

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
        	
        end_time = time.clock()
        print '\n\tTotal Time: %s sec' % (end_time - start_time)
 

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
		(users, passwords, clients) = create_test_view_setup(create_petreports=False)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			user = users [user_i]
			client = clients [client_i]

			print "[INFO]:%s logs onto %s to render the profile page..." % (user, client)

			loggedin = client.login(username = users [user_i].username, password = passwords[user_i])
			self.assertTrue(loggedin == True)
			response = client.get(URL_USERPROFILE + str(user.id) + '/')

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
			(user,password) = create_random_User(i,pretty_name=True)
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
			(user,password) = create_random_User(i,pretty_name=True)
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
		
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		performance_report(iteration_time)
		

'''===================================================================================
FollowTesting: Testing for EPM Following and Unfollowing functionalities
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

    def test_following_and_unfollowing_a_user(self):
        print "\n>>>> Testing 'test_following_and_unfollowing_a_user' for %d iterations " % NUMBER_OF_TESTS

        iteration_time = 0.00

        # Need to setup clients, users, and their passwords in order to simula the following function.
        (users, passwords, clients) = create_test_view_setup(create_petreports=False, create_petmatches=False)
        print users
        for i in range (NUMBER_OF_TESTS):
            start_time = time.clock()

			# indexes
            user_one_i = random.randrange(0, NUMBER_OF_TESTS)
            user_two_i = random.randrange(0, NUMBER_OF_TESTS)
            if user_one_i == user_two_i: 
            	continue
            client_i = random.randrange(0, NUMBER_OF_TESTS)

            # objects
            user_one = users [user_one_i]
            password_one = passwords [user_one_i]
            client = clients [client_i]
            user_two = users [user_two_i]
            password_two = passwords [user_two_i]
            print "\n%s ............................................................." % i
            print "  %s (id:%s) and %s (id:%s) have been created." % (user_one, user_one.id, user_two, user_two.id)

			#Log onto the first user.
            client = clients [client_i]
            loggedin = client.login(username = user_one.username, password = password_one)
            self.assertTrue(loggedin == True)			
            print "  %s logs onto %s to follow %s." % (user_one, client, user_two)

            # Go to the second user's profile page
            response = client.get(URL_USERPROFILE + str(user_two.id) + "/")
            self.assertEquals(response.status_code, 200)

            # ...................Testing Following Function.........................

            # Make the POST request Call for following the second user
            follow_url = URL_FOLLOW + str(user_one.id) + "/" + str(user_two.id) + "/"
            post = {'userprofile_id1': user_one.id, 'userprofile_id2': user_two.id}
            response = client.post(follow_url, post, follow=True)

			# Make assertions
            self.assertEquals(response.status_code, 200)
            self.assertTrue(len(response.redirect_chain) == 2)
            self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/UserProfile/'+ str(user_two.id) )
            self.assertEquals(response.redirect_chain[0][1], 302)
            self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(user_two.id) + "/")

            # Assert that 
            # the second user is in the first user's following list, and 
            # the first user is in the second user's followers list
            self.assertTrue(user_two.userprofile in user_one.userprofile.following.all())
            self.assertTrue(user_one.userprofile in user_two.userprofile.followers.all())
            print "  %s first followed %s." % (user_one, user_two)
 
            # ...................Testing Unfollowing Function.........................

            # Make the POST request Call for unfollowing the second user
            unfollow_url = URL_UNFOLLOW + str(user_one.id) + "/" + str(user_two.id) + "/"
            post = {'userprofile_id1': user_one.id, 'userprofile_id2': user_two.id}
            response = client.post(unfollow_url, post, follow=True)

			# Make assertions
            self.assertEquals(response.status_code, 200)
            self.assertTrue(len(response.redirect_chain) == 2)
            self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/UserProfile/'+ str(user_two.id) )
            self.assertEquals(response.redirect_chain[0][1], 302)
            self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(user_two.id) + "/")
 
            # Assert that 
            # the second user is not in the first user's following list, and 
            # the first user is not in the second user's followers list
            self.assertTrue(not user_two.userprofile in user_one.userprofile.following.all())
            self.assertTrue(not user_one.userprofile in user_two.userprofile.followers.all())
            print "  %s then unfollowed %s." % (user_one, user_two)

            # Logout the first user
            client.logout()

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

	def test_log_account_creations(self):
		print_testing_name("test_log_account_creations")
		iteration_time = 0.00

		for i in range(NUMBER_OF_TESTS):
			start_time = time.clock()
			(user, password) = create_random_User(i, pretty_name=True)
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
		(users, passwords, clients) = create_test_view_setup()

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)

			#Create and submit a Pet Report object as form content
			pr = create_random_PetReport(users [user_i])

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
		(users, passwords, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

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
		(users, passwords, clients) = create_test_view_setup(create_petreports=False, create_petmatches=False)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_one_i = random.randrange(0, NUMBER_OF_TESTS)
			user_two_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)

			if user_one_i == user_two_i:
				continue

			#objects
			user_one = users [user_one_i]
			password_one = passwords [user_one_i]
			user_two = users [user_two_i]
			password_two = passwords [user_two_i]

			print "[INFO]:%s (id:%s) and %s (id:%s) have been created." % (user_one, user_one.id, user_two, user_two.id)

			#Log in First.
			client = clients [client_i]
			loggedin = client.login(username = user_one.username, password = password_one)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to follow %s." % (user_one, client, user_two)			

			# Go to the second user's profile page
			response = client.get(URL_USERPROFILE + str(user_two.id) + "/")
			self.assertEquals(response.status_code, 200)

			# Make the POST request Call for following the second user
			follow_url = URL_FOLLOW + str(user_one.id) + "/" + str(user_two.id) + "/"
			post = {'userprofile_id1': user_one.id, 'userprofile_id2': user_two.id}
			response = client.post(follow_url, post, follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()						

			# Check if the activity for following a UserProfile appears in this user_one's log.
			self.assertTrue(activity_has_been_logged(ACTIVITY_FOLLOWING, userprofile=user_one.get_profile(), userprofile2=user_two.get_profile()) == True)		
			print "[INFO]:%s has followed %s" % (user_one.username, user_two.username)

			# Check if the activity for following a UserProfile appears in this user_two's log.
			self.assertTrue(activity_has_been_logged(ACTIVITY_FOLLOWER, userprofile=user_two.get_profile(), userprofile2=user_one.get_profile()) == True)				
			print "[INFO]:%s has been followed by %s" % (user_two.username, user_one.username)
	
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
		(users, passwords, clients) = create_test_view_setup(create_petreports=False, create_petmatches=False)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_one_i = random.randrange(0, NUMBER_OF_TESTS)
			user_two_i = random.randrange(0, NUMBER_OF_TESTS)

			if user_one_i == user_two_i:
			    continue

			client_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user_one = users [user_one_i]
			password_one = passwords [user_one_i]
			user_two = users [user_two_i]
			password_two = passwords [user_two_i]

			print "[INFO]:%s (id:%s) and %s (id:%s) have been created." % (user_one, user_one.id, user_two, user_two.id)

			#Log in First.
			client = clients [client_i]
			loggedin = client.login(username = user_one.username, password = password_one)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to follow %s." % (user_one, client, user_two)			

			# Go to the second user's profile page
			response = client.get(URL_USERPROFILE + str(user_two.id) + "/")
			self.assertEquals(response.status_code, 200)

			# Make the POST request Call for following the second user
			follow_url = URL_FOLLOW + str(user_one.id) + "/" + str(user_two.id) + "/"
			post = {'userprofile_id1': user_one.id, 'userprofile_id2': user_two.id}
			response = client.post(follow_url, post, follow=True)
			self.assertEquals(response.status_code, 200)

			# Make the POST request Call for unfollowing the second user
			unfollow_url = URL_UNFOLLOW + str(user_one.id) + "/" + str(user_two.id) + "/"
			post = {'userprofile_id1': user_one.id, 'userprofile_id2': user_two.id}
			response = client.post(unfollow_url, post, follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()						

			# Check if the activity for unfollowing a UserProfile appears in this user_one's log.
			self.assertTrue(activity_has_been_logged(ACTIVITY_UNFOLLOWING, userprofile=user_one.get_profile(), userprofile2=user_two.get_profile()) == True)			
			print "[INFO]:%s has unfollowed %s" % (user_one.username, user_two.username)
				
			# Check if the activity for unfollowing a UserProfile appears in this user_two's log.
			self.assertTrue(activity_has_been_logged(ACTIVITY_UNFOLLOWER, userprofile=user_two.get_profile(), userprofile2=user_one.get_profile()) == True)			
			print "[INFO]:%s has been unfollowed by %s" % (user_two.username, user_one.username)
				
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
		(users, passwords, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]
			print "[INFO]:A user %s and a pet report %s have been created." % (user.userprofile, petreport)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the prdp interface to add a bookmark." % (user, client)			

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
			if(not previously_bookmarked):
				self.assertEquals(old_bookmarks_count, (new_bookmarks_count-1))

			# Check if the activity for adding a PetReport bookmark appears in this user's log.
			print "[INFO]:%s has added a bookmark for %s." % (user, petreport)
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
		(users, passwords, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]
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
			print "[INFO]:%s has removed a bookmark for %s." % (user, petreport)
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
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]

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
		(users, passwords, clients) = create_test_view_setup()

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			client_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			client = clients [client_i]
			
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
			self.assertTrue(num_activities >=0 and num_activities <= max_num_activities)

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
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			another_user_i = random.randrange(0, NUMBER_OF_TESTS)
			if user_i == another_user_i:
			    continue
			petreport_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			another_user = users [another_user_i]
			another_user_password = passwords [another_user_i]
			petreport = petreports [petreport_i]

			#Log into another_user.
			client = clients [client_i]
			loggedin = client.login(username = another_user.username, password = another_user_password)
			self.assertTrue(loggedin == True)

			# Make the POST request Call for another_user to follow the user
			follow_url = URL_FOLLOW + str(another_user.id) + "/" + str(user.id) + "/"
			post = {'userprofile_id1': another_user.id, 'userprofile_id2': user.id}
			response = client.post(follow_url, post, follow=True)
			self.assertEquals(response.status_code, 200)
			client.logout()	

			#Log into user.
			client = clients [client_i]
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)

			# Make the POST request Call for user to follow the another_user
			follow_url = URL_FOLLOW + str(user.id) + "/" + str(another_user.id) + "/"
			post = {'userprofile_id1': user.id, 'userprofile_id2': another_user.id}
			response = client.post(follow_url, post, follow=True)
			self.assertEquals(response.status_code, 200)

			# Make the POST request Call for user to add a bookmark for a random petreport
			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
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

