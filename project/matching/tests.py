from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from home.models import *
from utils import *
from constants import *
import unittest, string, random, sys, time

'''===================================================================================
MatchingTesting: Testing for EPM Matching
==================================================================================='''
class MatchingTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_get_matching_interface(self):
		print_testing_name("test_get_matching_interface")
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

			#Go to the PRDP Page
			prdp_url = URL_PRDP + str(petreport.id) + "/"
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], prdp_url)
			print "[SUCCESS]:%s has successfully requested page %s..." % (user, prdp_url)  

			#From here, go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)

			if response.status_code == 302:
				print "[INFO]:Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue
			else:
				self.assertEquals(response.status_code, 200)
				print "[SUCCESS]:%s has successfully requested page %s..." % (user, matching_url)  	
			
			self.assertEquals(response.request ['PATH_INFO'], matching_url)	
			client.logout()	
			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)			

	def test_get_propose_match_dialog (self):
		print_testing_name("test_get_propose_match_dialog")
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
			print matching_url
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print "[INFO]:Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue

			self.assertEquals(response.status_code, 200)
			print "[INFO]:%s has successfully requested page %s..." % (user, matching_url)  				

			#PetReport filters
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			candidate_petreport = random.choice(filtered_pet_reports)

			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], propose_match_url)			

			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)	


	def test_post_good_propose_match (self):
		print_testing_name("test_post_good_propose_match")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports) = create_test_view_setup(create_petreports=True)
		num_petmatches = 0

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
				print "[INFO]:Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
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

			#Grab the PetMatch that has either been posted in the past or has been posted by this User.
			match = PetMatch.get_PetMatch(petreport, candidate_petreport)
			if match.UserProfile_has_voted(user.get_profile()) == True:
				print "[OK]:A PetMatch already exists with these two PetReports, and so %s has up-voted this match!" % (user)
			else:
				print "[OK]: has successfully POSTED a new match!" % (user)				
				num_petmatches += 1

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(len(response.redirect_chain), 1)
			self.assertEquals(response.redirect_chain[0][0], 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertEquals(response.request ['PATH_INFO'], URL_HOME)				

			#Some checks for the PetMatch objects stored
			self.assertTrue(len(PetMatch.objects.all()) == num_petmatches or len(PetMatch.objects.all()) <= i)
			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		performance_report(iteration_time)


	def test_post_bad_propose_match (self):
		print_testing_name("test_post_bad_propose_match")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports) = create_test_view_setup(create_petreports=True)
		num_petmatches = 0

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
				print "[INFO]:Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue

			self.assertEquals(response.status_code, 200)
			print "[INFO]:%s has successfully requested page '%s'..." % (user, matching_url) 
			candidate_petreport = random.choice(filtered_pet_reports) 

			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print "[INFO]:%s has successfully requested page '%s'..." % (user, propose_match_url) 

			#The description is empty, so this POST should fail.
			description = "       "
			post = {'description': description}
			response = client.post(propose_match_url, post, follow=True)
			client.logout()					

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], propose_match_url)
			print "[INFO]:%s was NOT able to POST a successful match. That was to be expected!" % (user)

			#Some checks for the PetMatch objects stored
			self.assertTrue(len(PetMatch.objects.all()) == 0)
			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		performance_report(iteration_time)	




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
PetMatchTesting: Testing for EPM Pet Match functionality
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class PetMatchTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()


	def test_get_PetMatch_dialog_page (self):
		print_testing_name("test_get_PetMatch_dialog_page")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, NUMBER_OF_TESTS)
			petmatch_i = random.randrange(0, NUMBER_OF_TESTS/2)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]
			petmatch = petmatches [petmatch_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the PMDP..." % (user, client)

			#Go to the PRDP
			prdp_url = URL_PRDP + str(petreport.id) + "/"
			response = client.get(prdp_url)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], prdp_url)
			print "[INFO]:%s enters the Pet Report Detailed Page successfully" % (user)

			#Now go to the PMDP
			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			response = client.get(pmdp_url)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], pmdp_url)
			print "[INFO]:%s enters the Pet Match Detailed Page successfully" % (user)

			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)	


	def test_post_good_PetMatch_upvote (self):
		print_testing_name("test_post_good_PetMatch_upvote")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petmatch_i = random.randrange(0, NUMBER_OF_TESTS/2)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petmatch = petmatches [petmatch_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the PMDP..." % (user, client)

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
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)	


	def test_post_good_PetMatch_downvote (self):
		print_testing_name("test_post_good_PetMatch_downvote")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petmatch_i = random.randrange(0, NUMBER_OF_TESTS/2)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petmatch = petmatches [petmatch_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the PMDP..." % (user, client)

			pmdp_url = URL_PMDP + str(petmatch.id) + "/"
			print pmdp_url
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
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)


