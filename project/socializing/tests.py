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
from django.test import TestCase

'''===================================================================================
UserProfileTesting: Testing for EPM User Profile Page
==================================================================================='''
class UserProfileTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_render_UserProfile_page(self):
		print_testing_name("test_render_UserProfile_page")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate accessing UserProfile pages.
		results = setup_objects(delete_all_objects=False)
		users = results ['users']
		clients = results['clients']

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
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)


	def test_send_message_to_UserProfile(self):
		print_testing_name ("test_send_message_to_UserProfile")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords.
		results = setup_objects(delete_all_objects=False)
		users = results ['users']
		clients = results ['clients']

		#We assume that the subject's email address is formatted properly and is a real email address.
		#For testing purposes, we dump email messages to file and assert that their contents are correct.
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			user_one, password_one = random.choice(users)
			user_two, password_two = random.choice(users)
			userprofile_one = user_one.userprofile
			userprofile_two = user_two.userprofile
			client = random.choice(clients)

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
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)
	
	def test_editUserProfile_savePassword(self):
		print_testing_name("test_editUserProfile_savePassword")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = create_random_User(i)
			client = Client (enforce_csrf_checks=False)
			user_i = user.id

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print_test_msg("%s logs onto %s to enter the EditUserProfile page..." % (user, client))
			
			#Navigate to the EditUserProfile_form page
			response = client.get(URL_EDITUSERPROFILE)
			self.assertEquals(response.status_code, 200) 
			self.assertTrue(response.request ['PATH_INFO'] == URL_EDITUSERPROFILE)

			#Change the user's password
			new_password1 = generate_string (User._meta.get_field('password').max_length)
			new_password2 = generate_string (User._meta.get_field('password').max_length)

			#send the post request where the new_password1 & new_password2 do not match
			post =  {"action":"savePassword", "old_password":password, "new_password1":new_password1, "new_password2":new_password2}
			response = client.post(URL_EDITUSERPROFILE_PWD, post, follow=True)
			user = User.objects.get(pk=user_i)

			#The password shouldn't have changed
			self.assertEquals(response.status_code, 200) 
			self.assertFalse(user.check_password(new_password1))
			self.assertTrue(user.check_password(password))

			#send the post request where the old password is not correct
			post =  {"action":"savePassword", "old_password":new_password1, "new_password1":new_password1, "new_password2":new_password1}
			
			response = client.post(URL_EDITUSERPROFILE_PWD, post, follow=True)
			user = User.objects.get(pk=user_i)
			#the password shouldn't have changed
			self.assertEquals(response.status_code, 200) 
			self.assertTrue(user.check_password(password))
			self.assertFalse(user.check_password(new_password1))

			#send the post request to change the password
			post =  {"action":"savePassword","old_password":password,"new_password1":new_password1,"new_password2":new_password1}
			
			response = client.post(URL_EDITUSERPROFILE_PWD, post,follow=True)
			user = User.objects.get(pk=user_i)
			#the password shouldn't have changed
			self.assertEquals(response.status_code,200) 
			self.assertTrue(user.check_password(new_password1))

			print_test_msg("Test test_editUserProfile_savePassword was successful for user %s" % (user))
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			
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
			print_test_msg("%s logs onto %s to enter the EditUserProfile page..." % (user, client))

			#Edit the User's information and save it
			username = generate_string (User._meta.get_field('username').max_length)
			first_name = generate_string (User._meta.get_field('first_name').max_length)
			last_name = generate_string (User._meta.get_field('last_name').max_length)
			description = generate_string (UserProfile._meta.get_field("description").max_length)

			#email = user.email
			email = TEST_EMAIL 

			#Navigate to the EditUserProfile_form page
			response = client.get(URL_EDITUSERPROFILE)
			#Assert that the page was navigated to.
			self.assertEquals(response.status_code,200) 
			self.assertTrue(response.request ['PATH_INFO'] == URL_EDITUSERPROFILE)

			#the post data
			post =  {"action":"saveProfile","username":username,"first_name":first_name,"last_name":last_name,"email":email, "description":description}
			#send the post request with the changes
			response = client.post(URL_EDITUSERPROFILE_INFO, post, follow=True)
			
			user = User.objects.get(pk=user_i)
			
			self.assertEquals(response.status_code,200) 
			#IF USERNAME EXISTS, NOTHING SHOULD CHANGE
			self.assertEquals(user.username,username)
			self.assertEquals(user.first_name,first_name)
			self.assertEquals(user.last_name,last_name)

			edituserprofile = EditUserProfile.objects.get(user=user)
			email_verification_url = URL_EMAIL_VERIFICATION_COMPLETE + edituserprofile.activation_key + "/"
			#navigate to verify the new email address
			response = client.get(email_verification_url)
			self.assertEquals(response.status_code,302)
			#assert that the user's email address has changed
			user = User.objects.get(pk=user_i)
			self.assertEquals(user.email,email)

			print_test_msg("test_editUserProfile_saveProfile was successful for user %s" % (user))
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			
		performance_report(iteration_time)
		

'''===================================================================================
FollowingTesting: Testing for EPM Following and Unfollowing functionalities
==================================================================================='''
class FollowingTesting (unittest.TestCase):

    # Get rid of all objects in the QuerySet.
    def setUp(self):
       delete_all(leave_Users=False)

    # Get rid of all objects in the QuerySet.
    def tearDown(self):
    	delete_all(leave_Users=False)

    def test_following_and_unfollowing_a_UserProfile(self):
    	print_testing_name("test_following_and_unfollowing_a_UserProfile")
        iteration_time = 0.00

        # Need to setup clients, users, and their passwords in order to simula the following function.
        results  = setup_objects()
        users = results ['users']
        clients = results ['clients']
        
        for i in range (NUMBER_OF_TESTS):
            start_time = time.clock()

            user_one, password_one = random.choice(users)
            user_two, password_two = random.choice(users)
            userprofile_one = user_one.userprofile
            userprofile_two = user_two.userprofile
            client = random.choice(clients)

            if user_one.id == user_two.id:
            	continue

			#Log onto the first user.
            loggedin = client.login(username = userprofile_one.user.username, password = password_one)
            self.assertTrue(loggedin == True)			
            print_test_msg ("%s logs onto %s to follow %s" % (userprofile_one.user.username, client, userprofile_two.user.username))

            # Go to the second user's profile page
            response = client.get(URL_USERPROFILE + str(userprofile_two.id) + "/")
            self.assertEquals(response.status_code, 200)

            # ...................Testing Following Function.........................

            # Make the POST request Call for following the second user
            post = {"target_userprofile_id": userprofile_two.id}
            response = client.post(URL_FOLLOW, post, follow=True)

			# Make assertions
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.redirect_chain[0][0], 'http://testserver/users/'+ str(userprofile_two.id))
            self.assertEquals(response.redirect_chain[0][1], 302)
            self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(userprofile_two.id) + "/")

            # Assert that 
            # the second user is in the first user's following list, and 
            # the first user is in the second user's followers list
            self.assertTrue(userprofile_two in userprofile_one.following.all())
            self.assertTrue(userprofile_one in userprofile_two.followers.all())
            print_test_msg ("%s has followed %s" % (userprofile_one.user.username, userprofile_two.user.username))
 
            # ...................Testing Unfollowing Function.........................

            # Make the POST request Call for unfollowing the second user
            post = {"target_userprofile_id": userprofile_two.id}
            response = client.post(URL_UNFOLLOW, post, follow=True)

			# Make assertions
            self.assertEquals(response.status_code, 200)
            self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/users/'+ str(userprofile_two.id))
            self.assertEquals(response.redirect_chain[0][1], 302)
            self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(userprofile_two.id) + "/")
 
            # Assert that 
            # the second user is not in the first user's following list, and 
            # the first user is not in the second user's followers list
            self.assertTrue(not userprofile_two in userprofile_one.following.all())
            self.assertTrue(not userprofile_one in userprofile_two.followers.all())
            print_test_msg ("%s then unfollowed %s" % (userprofile_one.user.username, userprofile_two.user.username))

            # Logout the first user
            client.logout()
            output_update(i + 1)
            end_time = time.clock()
            iteration_time += (end_time - start_time)

        self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
        self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
        performance_report(iteration_time)

'''===================================================================================
ReputationTesting: Testing for EPM User Reputation Points
==================================================================================='''
class ReputationTesting(unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_reputation_points_for_upvoting_PetMatch (self):
		print_testing_name("test_reputation_points_for_upvoting_PetMatch")
		iteration_time = 0.00

		results = setup_objects(create_petreports=True, create_petmatches=True)
		users = results ["users"]
		clients = results ["clients"]
		petreports = results ["petreports"]
		petmatches = results ["petmatches"]

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
			print_test_msg ("%s logs onto %s to enter the PMDP..." % (user, client))

			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			response = client.get(pmdp_url)
			
			print_test_msg ("Reputation points for %s BEFORE upvoting: %s" % (user, old_reputation))
			print_test_msg ("Reputation points for %s (who proposed this PetMatch) BEFORE upvoting: %s" %(pm_proposed_by_user, p_old_reputation))
			print_test_msg ("Voted or not for this petmatch before: %s" % petmatch.UserProfile_has_voted(user.userprofile))
			
			# check if the user has voted before or not and set the 'voted' flag accordingly
			if petmatch.UserProfile_has_voted(user.userprofile) is False:
				voted = False
				print_test_msg ("User has NEVER voted for this petmatch")
			else:
				voted = petmatch.UserProfile_has_voted(user.userprofile)
				print_test_msg ("User has Voted for this petmatch before")

			vote_url = URL_VOTE_MATCH
			post =  {"vote":"upvote", "match_id":petmatch.id, "user_id":user.id}
			response = client.post(vote_url, post, follow=True)

			# Reset user with a new fresh copy from the DB.
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)

			print_test_msg ("Reputation points for %s AFTER upvoting: %s" %(user, user.userprofile.reputation))
			pm_proposed_by_user = PetMatch.objects.get(pk=petmatch.id).proposed_by
			print_test_msg ("Reputation points for %s (who proposed this PetMatch) AFTER upvoting: %s" %(pm_proposed_by_user, pm_proposed_by_user.reputation))

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], vote_url)
			self.assertTrue(petmatch.UserProfile_has_voted(user.userprofile) == UPVOTE)
			self.assertEquals(petmatch.up_votes.get(pk=user.id), user.userprofile)

			if (voted == False) and (user.userprofile.id != pm_proposed_by_user.id):
				self.assertEquals(user.userprofile.reputation, old_reputation + REWARD_PETMATCH_VOTE)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation + REWARD_USER_PROPOSED_PETMATCH_VOTE)
			
			elif (voted == UPVOTE) and (user.userprofile.id != pm_proposed_by_user.id):
				self.assertEquals(user.userprofile.reputation, old_reputation)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation)

			elif (voted == DOWNVOTE) and (user.userprofile.id != pm_proposed_by_user.id):
				self.assertEquals(user.userprofile.reputation, old_reputation)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation + REWARD_USER_PROPOSED_PETMATCH_VOTE)
			
			elif (voted == False) and (user.userprofile.id == pm_proposed_by_user.id):
				self.assertEquals(user.userprofile.reputation, old_reputation + REWARD_PETMATCH_VOTE + REWARD_USER_PROPOSED_PETMATCH_VOTE)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation + REWARD_PETMATCH_VOTE + REWARD_USER_PROPOSED_PETMATCH_VOTE)
			else:
				print_error_msg("Unexpected case...")
				self.assertFalse(True) #Should fail.

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)


	def test_reputation_points_for_downvoting_PetMatch (self):
		print_testing_name("test_reputation_points_for_downvoting_PetMatch")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects
		results = setup_objects(create_petreports=True, create_petmatches=True)
		users = results ["users"]
		clients = results ["clients"]
		petreports = results ["petreports"]
		petmatches = results ["petmatches"]

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
			print_test_msg ("%s logs onto %s to enter the PMDP..." % (user, client))

			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			response = client.get(pmdp_url)
			
			print_test_msg ("Reputation points BEFORE downvoting: %s" % (old_reputation))
			print_test_msg ("Voted or not for this petmatch before: %s" % petmatch.UserProfile_has_voted(user.userprofile))
			print_test_msg ("Reputation points for %s (who proposed this PetMatch) BEFORE downvoting: %s" % (pm_proposed_by_user, p_old_reputation))
			
			# check if the user has voted before or not and set the 'voted' flag accordingly
			if petmatch.UserProfile_has_voted(user.userprofile) is False:
				voted = False
				print_test_msg ("User has NEVER voted for this petmatch")
			elif petmatch.UserProfile_has_voted(user.userprofile) is not False:
				voted = petmatch.UserProfile_has_voted(user.userprofile)
				print_test_msg ("User has Voted for this petmatch before")
			else:
				print_error_msg ("Something is wrong!")
				self.assertFalse(True)

			vote_url = URL_VOTE_MATCH
			post =  {"vote":"downvote", "match_id":petmatch.id, "user_id":user.id}
			response = client.post(vote_url, post, follow=True)

			# Reset user with a new fresh copy from the DB
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)

			print_test_msg ("Reputation points AFTER downvoting: %s" %(user.userprofile.reputation))
			pm_proposed_by_user = PetMatch.objects.get(pk=petmatch.id).proposed_by
			print_test_msg ("Reputation points for %s (who proposed this PetMatch) AFTER downvoting: %s" %(pm_proposed_by_user, pm_proposed_by_user.reputation))

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], vote_url)
			self.assertTrue(petmatch.UserProfile_has_voted(user.userprofile) == DOWNVOTE)
			self.assertEquals(petmatch.down_votes.get(pk = user.id), user.userprofile)
			
			if (voted == False) and (user.userprofile.id != pm_proposed_by_user.id):
				self.assertEquals(user.userprofile.reputation, old_reputation + REWARD_PETMATCH_VOTE)
			
			elif (voted == DOWNVOTE) and (user.userprofile.id != pm_proposed_by_user.id):
				self.assertEquals(user.userprofile.reputation, old_reputation)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation)
			
			elif (voted == UPVOTE) and (user.userprofile.id != pm_proposed_by_user.id):
				self.assertEquals(user.userprofile.reputation, old_reputation)
			
			elif (not voted) and (user.userprofile.id == pm_proposed_by_user.id):
				self.assertEquals(user.userprofile.reputation, old_reputation + REWARD_PETMATCH_VOTE)
				self.assertEquals(pm_proposed_by_user.reputation, p_old_reputation + REWARD_PETMATCH_VOTE)
			else:
				print_error_msg ("Assert FAILED! Something is wrong!")
				self.assertFalse(True)

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)


	def test_reputation_points_for_submitting_PetReport(self):
		print_testing_name("test_reputation_points_for_submitting_PetReport")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(create_petreports=False)
		users = results ["users"]
		clients = results ["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			old_reputation = user.userprofile.reputation
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg ("%s logs onto %s to enter the pet report form..." % (user, client))

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

			print_test_msg ("Reputation points BEFORE submitting a PetReport: %s" %(old_reputation))

			#Make the POST request Call
			response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)

			# Reset user with a new fresh copy from the DB
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)
			print_test_msg ("Reputation points AFTER submitting a PetReport: %s" %(user.userprofile.reputation))

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertTrue(len(response.redirect_chain) == 1) 
			# self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)
			self.assertTrue(len(PetReport.objects.all()) == 2*i + 2)
			self.assertNotEquals(user.userprofile.reputation, old_reputation)
			self.assertEquals(user.userprofile.reputation, old_reputation + REWARD_PETREPORT_SUBMIT)
			client.logout()

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == 2*NUMBER_OF_TESTS) 
		performance_report(iteration_time)


	def test_reputation_points_for_proposing_PetMatch(self):
		print_testing_name("test_reputation_points_for_proposing_PetMatch")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(create_petreports=True)
		users = results ["users"]
		clients = results ["clients"]
		petreports = results ["petreports"]
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
			print_test_msg ("%s logs onto %s to enter the matching interface..." % (user, client))

			#Go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print_test_msg ("There are no PetReports to match this PetReport with - Back to the Home Page!")
				continue

			self.assertEquals(response.status_code, 200)
			print_test_msg ("%s has successfully requested page '%s'..." % (user, matching_url))
			candidate_petreport = random.choice(filtered_pet_reports) 

			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print_test_msg ("%s has successfully requested page '%s'..." % (user, propose_match_url))
			print_test_msg ("Reputation points BEFORE proposing a PetMatch: %s" %(old_reputation))

			#Grab the PetMatch that is either a new one, has been posted in the past or has been posted by this User, and set the pm_status flag accordingly based on the activities.
			match = PetMatch.get_PetMatch(petreport, candidate_petreport)
			if match is not None:
				if match.UserProfile_has_voted(user.userprofile) is not False:
					print_test_msg ("A duplicate PetMatch, and %s has VOTED this match before! User will get no points." % (user))
					pm_status = None
				elif match.UserProfile_has_voted(user.userprofile) is False:
					print_test_msg ("A duplicate PetMatch, and %s has NEVER voted this match before! User will get voting points." % (user))
					pm_status = ACTIVITY_PETMATCH_UPVOTE
				else:
					print_error_msg ("Something went wrong with checking the UserProfile_has_voted function!")
					self.assertTrue(False)

			elif match is None:
				print_test_msg ("This will be a new PetMatch. User will get proposing points.")
				pm_status = ACTIVITY_PETMATCH_PROPOSED
			else:
				print_error_msg ("Something went wrong while checking of the 'match exists or not!")
				self.assertFalse(True)

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
			print_test_msg ("Reputation points AFTER proposing a PetMatch: %s" %(user.userprofile.reputation))

			#Grab the PetMatch, again, that has either been posted in the past or has been posted by this User.
			match = PetMatch.get_PetMatch(petreport, candidate_petreport)
			if match.UserProfile_has_voted(user.userprofile) is not False:
				print_test_msg ("A PetMatch already exists with these two PetReports, and so %s has up-voted this match!" % (user))
			else:
				print_test_msg ("%s has successfully POSTED a new match!" % (user))
				num_petmatches += 1

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(len(response.redirect_chain), 1)
			# self.assertEquals(response.redirect_chain[0][0], 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertEquals(response.request ['PATH_INFO'], URL_HOME)	
			if pm_status == ACTIVITY_PETMATCH_PROPOSED:
				self.assertEquals(user.userprofile.reputation, old_reputation+REWARD_PETMATCH_PROPOSE)
			elif pm_status == ACTIVITY_PETMATCH_UPVOTE:
				self.assertEquals(user.userprofile.reputation, old_reputation+REWARD_PETMATCH_VOTE)
			elif pm_status == None:
				self.assertEquals(user.userprofile.reputation, old_reputation)
			else:
				print_error_msg ("Assert Failed! Something went wrong with reputation points!")
				self.assertTrue(False)

			#Some checks for the PetMatch objects stored
			self.assertTrue(len(PetMatch.objects.all()) == num_petmatches or len(PetMatch.objects.all()) <= i)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			
		performance_report(iteration_time)


	def test_reputation_points_for_a_UserProfile_being_followed_and_unfollowed(self):
	    print_testing_name("test_reputation_points_for_a_UserProfile_being_followed_and_unfollowed")
	    iteration_time = 0.00

	    # Need to setup clients, users, and their passwords in order to simula the following function.
	    results = setup_objects(create_petreports=False, create_petmatches=False)
	    users = results ["users"]
	    clients = results ["clients"]
	        
	    for i in range (NUMBER_OF_TESTS):
	        start_time = time.clock()

	        # objects
	        user_one, password_one = random.choice(users)
	        user_two, password_two = random.choice(users)
	        userprofile_one = user_one.userprofile
	        userprofile_two = user_two.userprofile
	        old_reputation = userprofile_two.reputation
	        client = random.choice(clients)

	        if user_one.id == user_two.id:
	        	continue

	        print_test_msg("%s (id:%s) and %s (id:%s) have been created." % (userprofile_one, userprofile_one.id, userprofile_two, userprofile_two.id))

			#Log onto the first user.
	        loggedin = client.login(username = userprofile_one.user.username, password = password_one)
	        self.assertTrue(loggedin == True)			
	        print_test_msg ("%s logs onto %s to follow %s." % (userprofile_one.user.username, client, userprofile_two.user.username))

	        # Go to the second user's profile page
	        response = client.get(URL_USERPROFILE + str(userprofile_two.id) + "/")
	        self.assertEquals(response.status_code, 200)

	        print_test_msg ("Reputation points for %s BEFORE being followed: %s" %(userprofile_two, old_reputation))

	        # ...................Testing Following Function.........................

	        # Make the POST request Call for following the second user
	        post = {"target_userprofile_id": userprofile_two.id}
	        response = client.post(URL_FOLLOW, post, follow=True)

	        # Reset userprofile_two with a new fresh copy from the db
	        userprofile_two = UserProfile.objects.get(pk=user_two.id)
	        print_test_msg ("Reputation points for %s AFTER being followed: %s" %(userprofile_two, userprofile_two.reputation))

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
	        print_test_msg ("%s has followed %s." % (userprofile_one.user.username, userprofile_two.user.username))

	        # ...................Testing Unfollowing Function.........................

	        # reset old_reputation with a new fresh copy from the db
	        old_reputation = userprofile_two.reputation
	        print_test_msg ("Reputation points for %s BEFORE being unfollowed: %s" %(userprofile_two, old_reputation))

	        # Make the POST request Call for unfollowing the second user
	        post = {"target_userprofile_id": userprofile_two.id}
	        response = client.post(URL_UNFOLLOW, post, follow=True)

	        # reset userprofile_two with a new fresh copy from the db
	        userprofile_two = UserProfile.objects.get(pk=user_two.id)
	        print_test_msg ("Reputation points for %s AFTER being unfollowed: %s" %(userprofile_two, userprofile_two.reputation))

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
	        print_test_msg ("%s then unfollowed %s." % (userprofile_one, userprofile_two))

	        self.assertEquals(userprofile_two.reputation, old_reputation-REWARD_USER_FOLLOWED)

	        # Logout the first user
	        client.logout()
	        end_time = time.clock()
	        output_update(i + 1)
	        iteration_time += (end_time - start_time)

	    self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
	    self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
	    performance_report(iteration_time)


	def test_reputation_points_for_adding_and_removing_PetReport_bookmark(self):
		print_testing_name("test_reputation_points_for_adding_and_removing_PetReport_bookmark")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate bookmarking of PetReport objects.
		results = setup_objects(create_petreports=True)
		users = results ['users']
		clients = results ['clients']
		petreports = results ['petreports']

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
			print_test_msg ("%s logs onto %s to enter the PRDP..." % (user, client))

			#navigate to the prdp
			prdp_url = URL_PRDP + str(petreport.id) + "/"
			response = client.get(prdp_url)

			# ...................Testing Adding a Bookmark.........................
			print_test_msg ("Reputation points BEFORE bookmarking a PetReport: %s" %(old_reputation))

			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
			old_bookmarks_count = user.userprofile.bookmarks_related.count()

			# reset user with a new fresh copy from the db
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)

			print_test_msg ("Reputation points AFTER bookmarking a PetReport: %s" %(user.userprofile.reputation))

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], add_bookmark_url)
			self.assertEquals(user.userprofile.reputation, old_reputation+REWARD_PETREPORT_BOOKMARK)


			# ...................Testing Removing a Bookmark.........................
			old_reputation = user.userprofile.reputation
			print_test_msg ("Reputation points BEFORE unbookmarking a PetReport: %s" %(old_reputation))

			remove_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Remove Bookmark"}
			response = client.post(remove_bookmark_url, post, follow=True)
			new_bookmarks_count = user.userprofile.bookmarks_related.count()

			# Reset user with a new fresh copy from the db
			# Then stick the updated (user,password) combo back into the users list for easy referencing later.
			user = User.objects.get(pk=user.id)
			user_index = [u[0] for u in users].index(user)
			users[user_index] = (user, password)

			print_test_msg ("Reputation points AFTER unbookmarking a PetReport: %s" %(user.userprofile.reputation))

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], remove_bookmark_url)
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))
			self.assertEquals(user.userprofile.reputation, old_reputation-REWARD_PETREPORT_BOOKMARK)

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)

	def test_reputation_points_for_PetMatch_verification(self):
		print_testing_name = ("test_reputation_points_for_PetMatch_verification")
		iteration_time = 0.00
		# setup clients, users and their passwords
		results = setup_objects(create_petreports=True, create_petmatches=True)
		users = results ['users']
		clients = results ['clients']
		petreports = results ['petreports']
		petmatches = results ['petmatches']

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

				# log in first
				loggedin = client.login(username = user.username, password = password)
				self.assertTrue(loggedin == True)
				print_test_msg ("%s logs onto %s to enter the verification page..." % (user, client))
				print_test_msg ('petmatch users: %s, %s ' % (str(petmatch.lost_pet.proposed_by.user), str(petmatch.found_pet.proposed_by.user)))
				verification_page_url = URL_VERIFY_PETMATCH + str(petmatch.id) + "/"

				response = client.get(verification_page_url)
				userprofile = user.userprofile
				self.assertEquals(response.status_code, 200)

				print_test_msg ("PetMatch owner (%s) reputation BEFORE: %s " % (petmatch_owner.user, reputation[0]))
				print_test_msg ("Lost pet contact (%s) reputation BEFORE: %s " % (lost_pet_contact.user, reputation[1]))
				print_test_msg ("Found pet contact (%s) reputation BEFORE: %s " % (found_pet_contact.user, reputation[2]))

				old_verification_vote = int(petmatch.verification_votes[0])
				old_verification_votes = str(petmatch.verification_votes)
				print_test_msg ("OLD verification vote: %s" %old_verification_vote)
				print_test_msg ("OLD verification votes: %s" %old_verification_votes)

				print_test_msg ("----UPVOTERS----")
				for upvoters in petmatch.up_votes.all():
					print_test_msg ("%s reputation BEFORE: %s" %(upvoters.user, upvoters.reputation))
				print_test_msg ("----------------")
				
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

				print_test_msg ("NEW verification vote: %s" % new_verification_vote)
				print_test_msg ("NEW verification votes: %s" % new_verification_votes)
				print_test_msg ("Is successful: %s" % petmatch.is_successful)
				print_test_msg ("PetMatch owner (%s) reputation AFTER: %s " % (petmatch_owner.user, petmatch_owner.reputation))
				print_test_msg ("Lost pet contact (%s) reputation AFTER: %s " % (lost_pet_contact.user, lost_pet_contact.reputation))
				print_test_msg ("Found pet contact (%s) reputation AFTER: %s " % (found_pet_contact.user, found_pet_contact.reputation))
				
				print_test_msg ("----UPVOTERS----")
				for upvoters in petmatch.up_votes.all():
					print_test_msg ("%s reputation AFTER: %s" %(upvoters.user, upvoters.reputation))
				print_test_msg ("----------------")

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

			output_update(i+1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)        