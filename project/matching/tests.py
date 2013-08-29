from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from home.models import *
from utils import *
from constants import *
from pprint import pprint
import unittest, string, random, sys, time
from django.contrib.messages import constants as messages

'''===================================================================================
MatchingTesting: Testing for EPM Matching
==================================================================================='''
class MatchingTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)

	'''test if the list of candidate pet reports displayed on the matching interface 
	is ordered according to the number of matching attributes'''
	def test_get_ordered_candidate_matches(self):
		print_testing_name("test_get_ordered_candidate_matches")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_petreports=True)
		users = results['users']
		clients = results['clients']
		petreports = results['petreports']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			
			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the matching interface..." % (user, client))

			#From here, go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			#First, make the GET call to the non-ajax view function branch.
			response = client.get(matching_url)
			#Next, make the AJAX GET Call to reference those candidate petreports.
			candidate_strings = client.get(matching_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

			if response.status_code == 200:
				#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
				candidates = petreport.get_candidate_PetReports()

				if candidates is None:
					self.assertEquals(response.status_code, 302)
					print_test_msg("Oh! There are no PetReports to match this PetReport with - Back to the Home Page!")
					continue

				candidate_matches = petreport.get_ranked_PetReports(candidates=candidates)

				for k in range (NUMBER_OF_TESTS):
					a = random.randint(0, len(candidate_matches) - 1)
					b = random.randint(0, len(candidate_matches) - 1)
					if (a > b):
						self.assertTrue(petreport.compare (candidate_matches[a]) <= petreport.compare (candidate_matches[b]))
					else:
						self.assertTrue(petreport.compare (candidate_matches[a]) >= petreport.compare (candidate_matches[b]))
				print_info_msg("Ordering on Attribute-matched candidate pets verified for this petreport!\n")

			end_time = time.clock()
			iteration_time += end_time - start_time
			output_update(i + 1)
		performance_report(iteration_time)

	def test_get_matching_interface(self):
		print_testing_name("test_get_matching_interface")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_petreports=True)
		users = results['users']
		clients = results['clients']
		petreports = results['petreports']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the matching interface..." % (user, client))

			#Go to the PRDP Page
			prdp_url = URL_PRDP + str(petreport.id) + "/"
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], prdp_url)
			print_success_msg("%s has successfully requested page %s..." % (user, prdp_url))  

			#From here, go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)

			if response.status_code == 302:
				print_test_msg("Oh! There are no PetReports to match this PetReport with - Back to the Home Page!")
				continue
			else:
				self.assertEquals(response.status_code, 200)
				print_success_msg("%s has successfully requested page %s..." % (user, matching_url))  	
			
			self.assertEquals(response.request ['PATH_INFO'], matching_url)	
			client.logout()	
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)		

	def test_UserProfile_added_to_PetReport_workers_list(self):
		print_testing_name("test_UserProfile_added_to_PetReport_workers_list")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_petreports=True)
		users = results['users']
		clients = results['clients']
		petreports = results['petreports']

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the matching interface..." % (user, client))

			#Go to the PRDP Page
			prdp_url = URL_PRDP + str(petreport.id) + "/"
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], prdp_url)
			print_success_msg("%s has successfully requested page %s..." % (user, prdp_url)) 

			#From here, go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)

			if response.status_code == 302:
				print_test_msg("Oh! There are no PetReports to match this PetReport with - Back to the Home Page!")
				continue
			else:
				self.assertEquals(response.status_code, 200)
				print_test_msg("%s has successfully requested page %s..." % (user, matching_url))  	
			
			self.assertEquals(response.request ['PATH_INFO'], matching_url)	
			self.assertTrue(user.get_profile() in petreport.workers.all())
			self.assertTrue(petreport in user.get_profile().workers_related.all())
			client.logout()	
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)				

	def test_get_propose_PetMatch_dialog (self):
		print_testing_name("test_get_propose_PetMatch_dialog")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_petreports=True)
		users = results["users"]
		clients = results["clients"]
		petreports = results["petreports"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the matching interface..." % (user, client))

			#Go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			print matching_url
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			candidates = petreport.get_candidate_PetReports()

			if candidates is None:
				self.assertEquals(response.status_code, 302)
				print_test_msg("Oh! There are no PetReports to match this PetReport with - Back to the Home Page!")
				continue

			filtered_pet_reports = petreport.get_ranked_PetReports(candidates=candidates)
			self.assertEquals(response.status_code, 200)
			print_success_msg("%s has successfully requested page %s..." % (user, matching_url))  				
			candidate_petreport = random.choice(filtered_pet_reports)

			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], propose_match_url)			
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)	


	def test_propose_good_PetMatch (self):
		print_testing_name("test_propose_good_PetMatch")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(delete_all_objects=False, create_petreports=True)
		users = results["users"]
		clients = results["clients"]
		petreports = results["petreports"]
		num_petmatches = 0

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the matching interface..." % (user, client))			

			#Go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			candidates = petreport.get_candidate_PetReports()

			if candidates is None:
				self.assertEquals(response.status_code, 302)
				print_test_msg("Oh! There are no PetReports to match this PetReport with - Back to the Home Page!")
				continue

			filtered_pet_reports = petreport.get_ranked_PetReports(candidates=candidates)
			candidate_petreport = random.choice(filtered_pet_reports) 
			self.assertEquals(response.status_code, 200)
			print_test_msg("%s has successfully requested page '%s'..." % (user, matching_url)) 
			
			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print_test_msg("%s has successfully requested page '%s'..." % (user, propose_match_url)) 

			#Make the POST request Call		
			description = generate_lipsum_paragraph(500)
			post = {'description': description}
			response = client.post(propose_match_url, post, follow=True)
			client.logout()						

			#Grab the PetMatch that has either been posted in the past or has been posted by this User.
			match = PetMatch.get_PetMatch(petreport, candidate_petreport)
			if match.UserProfile_has_voted(user.get_profile()) == True:
				print_test_msg("[OK]:A PetMatch already exists with these two PetReports, and so %s has up-voted this match!" % (user))
			else:
				print_test_msg("[OK]: has successfully POSTED a new match!" % (user))				
				num_petmatches += 1

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ["PATH_INFO"], URL_HOME)				
			self.assertTrue(len(PetMatch.objects.all()) == num_petmatches or len(PetMatch.objects.all()) <= i)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			
		performance_report(iteration_time)

'''===================================================================================
PetMatchTesting: Testing for EPM PetMatch-ing functionality
==================================================================================='''
class PetMatchTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)


	def test_get_PetMatch_dialog_page (self):
		print_testing_name("test_get_PetMatch_dialog_page")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		result = setup_objects(delete_all_objects=False, create_petreports=True, create_petmatches=True)
		users = result["users"]
		clients = result["clients"]
		petreports = result["petreports"]
		petmatches = result["petmatches"]
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)
			petmatch = random.choice(petmatches)
			print_test_msg("PetMatch: %s" % petmatch)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the PMDP..." % (user, client))

			#Go to the PRDP
			prdp_url = URL_PRDP + str(petreport.id) + "/"
			response = client.get(prdp_url)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], prdp_url)
			print_test_msg("%s enters the Pet Report Detailed Page successfully" % (user))

			#Now go to the PMDP
			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			response = client.get(pmdp_url)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], pmdp_url)
			print("%s enters the Pet Match Detailed Page successfully" % (user))

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)	


	def test_post_good_PetMatch_upvote (self):
		print_testing_name("test_post_good_PetMatch_upvote")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		result = setup_objects(create_petreports=True, create_petmatches=True)
		users = result["users"]
		clients = result["clients"]
		petreports = result["petreports"]
		petmatches = result["petmatches"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petmatch = random.choice(petmatches)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print_test_msg("%s logs onto %s to enter the PMDP..." % (user, client))

			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			print pmdp_url
			response = client.get(pmdp_url)

			vote_url = URL_VOTE_MATCH
			post =  {"vote":"upvote", "match_id":petmatch.id, "user_id":user.id}
			response = client.post(vote_url, post, follow=True)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], vote_url)
			self.assertTrue(petmatch.UserProfile_has_voted(user.get_profile()) == UPVOTE)
			self.assertEquals(petmatch.up_votes.get(pk = user.id), user.get_profile())

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)	


	def test_post_good_PetMatch_downvote (self):
		print_testing_name("test_post_good_PetMatch_downvote")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects(create_petreports=True, create_petmatches=True)
		users = results["users"]
		clients = results["clients"]
		petreports = results["petreports"]
		petmatches = results["petmatches"]
		
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petmatch = random.choice(petmatches)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print_test_msg("%s logs onto %s to enter the PMDP..." % (user, client))

			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			print_test_msg(pmdp_url)
			response = client.get(pmdp_url)

			vote_url = URL_VOTE_MATCH
			post =  {"vote":"downvote", "match_id":petmatch.id, "user_id":user.id}
			response = client.post(vote_url, post, follow=True)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], vote_url)
			self.assertTrue(petmatch.UserProfile_has_voted(user.get_profile()) == DOWNVOTE)
			self.assertEquals(petmatch.down_votes.get(pk = user.id), user.get_profile())

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)



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
			
			verification_page_url = URL_VERIFY_PETMATCH + str(petmatch.id) + "/"
			print_test_msg(verification_page_url)
			response = client.get(verification_page_url)

			userprofile = user.get_profile()

			if response.status_code == 302:
				if petmatch.PetMatch_has_reached_threshold():
					self.assertFalse(( userprofile == petmatch.lost_pet.proposed_by) or (userprofile == petmatch.found_pet.proposed_by))
				
			#Looking for other users and their passwords in the users list.
			proposers = [petmatch.lost_pet.proposed_by.user, petmatch.found_pet.proposed_by.user]
			proposer = random.choice(proposers)
			userprofile = proposer.get_profile()
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

				userprofile = user.get_profile()

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







