from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from utilities.utils import *
from fixture import *
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
