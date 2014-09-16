from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from utilities.utils import *
from fixture import *
from pprint import pprint
from django.contrib.messages import constants as messages
from django.test import TestCase
import unittest, string, random, sys, time

'''===================================================================================
VerificationTesting: Testing for EPM Verification
==================================================================================='''
class VerificationTesting (unittest.TestCase):
	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_get_verification_page (self):
		print_testing_name("test_get_verification_page")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords
		result = setup_objects(create_petreports=True, create_petmatches=True)
		users = result['users']
		petmatches = result['petmatches']
		clients = result['clients']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
		
			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petmatch = random.choice(petmatches)

			#Log in First
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print_test_msg("%s logs onto %s to enter the verification page..." % (user, client))
			
			verification_page_url = URL_VERIFY_PETCHECK + str(petcheck.id) + "/"
			print_test_msg(verification_page_url)
			response = client.get(verification_page_url)

			userprofile = user.userprofile

			if response.status_code == 302:
				if petmatch.PetMatch_has_reached_threshold():
					self.assertFalse(( userprofile == petmatch.lost_pet.proposed_by) or (userprofile == petmatch.found_pet.proposed_by))
				
			#Looking for other users and their passwords in the users list.
			proposers = [petmatch.lost_pet.proposed_by.user, petmatch.found_pet.proposed_by.user]
			proposer = random.choice(proposers)
			userprofile = proposer.userprofile
			password = None

			for (user_obj, user_password) in users:
				if user_obj == proposer:
					password = user_password

			#Log in First
			loggedin = client.login(username = proposer.username, password = password)
			self.assertTrue(loggedin == True)			
			print_test_msg("%s logs onto %s to enter the verification page..." % (proposer, client))
			response = client.get(verification_page_url)

			if petmatch.PetMatch_has_reached_threshold() == True:
				self.assertEquals(response.status_code, 200)
				self.assertTrue((userprofile == petmatch.lost_pet.proposed_by) or (userprofile == petmatch.found_pet.proposed_by))

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)				
		performance_report(iteration_time)


	def test_post_verification_response(self):
		print_testing_name("test_post_verification_response")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords
		result = setup_objects(create_petreports=True, create_petmatches=True)
		petmatches = result["petmatches"]
		clients = result["clients"]
		users = result["users"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			
			#objects
			client = random.choice(clients)
			petmatch = random.choice(petmatches)
			petmatch_i = petmatches.index(petmatch)
			petmatch = PetMatch.objects.get(pk=petmatch.id)

			if petmatch.PetMatch_has_reached_threshold() == False:
				continue

			#If the test has been run for this pet match before then the current test run is disallowed
			if petmatch.verification_votes != '00':
				continue

			#Looking for other users and their passwords in the users list.
			proposers = [petmatch.lost_pet.proposed_by.user, petmatch.found_pet.proposed_by.user]
			lostpet_proposer_index = [user[0] for user in users].index(proposers[0])
			foundpet_proposer_index = [user[0] for user in users].index(proposers[1])

			for (user, password) in [users[lostpet_proposer_index], users[foundpet_proposer_index]]:

				#Log in First
				loggedin = client.login(username = user.username, password = password)
				self.assertTrue(loggedin == True)			
				print_test_msg("%s logs onto %s to enter the verification page..." % (user, client))
				
				print_test_msg('petmatch users: %s, %s ' % (str(petmatch.lost_pet.proposed_by.user),str(petmatch.found_pet.proposed_by.user)))

				verification_page_url = URL_VERIFY_PETMATCH + str(petmatch.id) + "/"
				print verification_page_url
				response = client.get(verification_page_url)

				userprofile = user.userprofile

				self.assertEquals(response.status_code,200)
				#user responds with a random message: either yes or no
				message = random.choice(['yes','no'])
				post = {'message':message}
				old_lost_pet_vote = petmatch.verification_votes[0]
				response = client.post(verification_page_url,post,follow = True)
				self.assertEquals(response.status_code,200)
				petmatch = PetMatch.objects.get(pk=petmatch.id)
				new_lost_pet_vote  = petmatch.verification_votes[0]
				if old_lost_pet_vote == '0':
					#sent_vote is 1 if message is yes and 2 if message is no
					sent_vote = '1' if (message == 'yes') else '2'if (message == 'no') else '0'
					self.assertEquals(sent_vote,new_lost_pet_vote)
				else:
					self.assertEquals(old_lost_pet_vote,new_lost_pet_vote)
				'''if the petmatch object is changed then the new version of the petmatch 
				object replaces the existing one in the petmatches list'''
				petmatches[petmatch_i] = petmatch
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)					
		performance_report(iteration_time)
				
				
	def test_function_PetMatch_has_reached_threshold(self):
		print_testing_name("test_function_PetMatch_has_reached_threshold")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords
		result = setup_objects(create_petreports=True, create_petmatches=True)
		petmatches = result["petmatches"]
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			petmatch = random.choice(petmatches)
			difference = petmatch.up_votes.count() - petmatch.down_votes.count()

			if difference >= PETMATCH_THRESHOLD:
				self.assertTrue(petmatch.PetMatch_has_reached_threshold())
			else:
				self.assertFalse(petmatch.PetMatch_has_reached_threshold())
				
			self.assertFalse(petmatch.verification_triggered)
			self.assertTrue(petmatch.is_open)			
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			
		performance_report(iteration_time)

	def test_function_verify_PetMatch(self):
		print_testing_name("test_function_verify_PetMatch")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords
		result = setup_objects(create_petreports=True, create_petmatches=True)
		petmatches = result["petmatches"]
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			petmatch = random.choice(petmatches)

			if petmatch.PetMatch_has_reached_threshold() == True:
				message = petmatch.verify_PetMatch()
				self.assertTrue(petmatch.verification_triggered)
				self.assertFalse(petmatch.is_open)
			else:
				self.assertFalse(petmatch.verification_triggered)
				self.assertTrue(petmatch.is_open)

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)

	def test_function_close_PetMatch(self):
		print_testing_name("test_function_close_PetMatch")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords
		result = setup_objects(create_petreports=True, create_petmatches=True)
		petmatches = result["petmatches"]
		clients = result["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			client = random.choice(clients)
			petmatch = random.choice(petmatches)
			verification_page_url = URL_VERIFY_PETMATCH + str(petmatch.id) + "/"
			print_debug_msg (petmatch)

			petmatch = PetMatch.objects.get(pk=petmatch.id)

			if petmatch.PetMatch_has_reached_threshold() == True:
				self.assertTrue(petmatch.verification_triggered)

				#if the pet match as already been closed, disallow the test from running for this pet match
				if petmatch.is_open == False:
					continue

				self.assertFalse(petmatch.is_open)
				old_pet_vote = petmatch.verification_votes
				#Looking for other users and their passwords in the users list.
				proposers = [petmatch.lost_pet.proposed_by.user, petmatch.found_pet.proposed_by.user]

				#Disallow the test from allowing the lost and found pet contacts to be the same person.
				if proposers[0] == proposers[1]:
					continue

				lostpet_proposer_index = [user[0] for user in users].index(proposers[0])
				foundpet_proposer_index = [user[0] for user in users].index(proposers[1])

				for (user, password) in [users[lostpet_proposer_index], users[foundpet_proposer_index]]:
					#Log in First
					loggedin = client.login(username = user.username, password = password)
					self.assertTrue(loggedin == True)			
					print_test_msg ("%s logs onto %s to enter the verification page..." % (user, client))
					user_response = random.randint(1,2)
					message = random.choice(['yes','no'])
					print_test_msg ("%s has responded with {%d, %s}" % (user, user_response, message))
					post = {'message':message}
					response = client.post(verification_page_url, post, follow = True)
					self.assertEquals(response.status_code, 200)

				petmatch = PetMatch.objects.get(pk=petmatch.id)
				lost_pet = PetReport.objects.get(pk=petmatch.lost_pet.id)
				new_pet_vote = petmatch.verification_votes
				self.assertTrue(petmatch.closed_date != None)

				if new_pet_vote == '11':
					self.assertTrue(petmatch.is_successful)
					self.assertTrue(lost_pet.closed)
					self.assertTrue(petmatch.found_pet.closed)

					for pm in petmatch.lost_pet.lost_pet_related.all(): 
						self.assertFalse(pm.is_open)
						self.assertTrue(pm.closed_date != None)

					for pm in petmatch.found_pet.found_pet_related.all(): 
						self.assertFalse(pm.is_open)
						self.assertTrue(pm.closed_date != None)

				else:
					self.assertFalse(petmatch.is_successful)

			print_success_msg("Pet Match has passed the test: test_function_verify_PetMatch")
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)







