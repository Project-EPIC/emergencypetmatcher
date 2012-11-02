from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from home.models import *
from utils import *
from constants import *
import unittest, string, random, sys, time
from django.contrib.messages import constants as messages

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
			print "PETMATCH: %s %d " % (petmatch, petmatch_i)


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

class VerificationTesting (unittest.TestCase):
	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_get_verification_page (self):
		print_testing_name("test_get_verification_page")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords
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

			#Log in First
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the verification page..." % (user, client)
			
			verification_page_url = URL_VERIFY_PETMATCH + str(petmatch.id) + "/"
			print verification_page_url
			response = client.get(verification_page_url)

			userprofile = user.get_profile()

			if response.status_code == 302:
				if petmatch.PetMatch_has_reached_threshold():
					self.assertFalse(( userprofile == petmatch.lost_pet.proposed_by) or (userprofile == petmatch.found_pet.proposed_by))
				else:
					self.assertFalse(petmatch.PetMatch_has_reached_threshold())	

			user_indexes = [users.index(petmatch.lost_pet.proposed_by.user),users.index(petmatch.found_pet.proposed_by.user)]
			user_i = random.choice(user_indexes)
			user = users[user_i]
			password = passwords[user_i]
			userprofile = user.get_profile()
			#Log in First
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "[INFO]:%s logs onto %s to enter the verification page..." % (user, client)
			response = client.get(verification_page_url)

			if petmatch.PetMatch_has_reached_threshold():
				self.assertEquals(response.status_code, 200)
				self.assertTrue(petmatch.PetMatch_has_reached_threshold())
				self.assertTrue(( userprofile == petmatch.lost_pet.proposed_by) or (userprofile == petmatch.found_pet.proposed_by))

	def test_post_verification_response(self):
		print_testing_name("test_post_verification_response")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			#indexes
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petmatch_i = random.randrange(0, NUMBER_OF_TESTS/2)
			
			#objects
			client = clients [client_i]
			petmatch = petmatches [petmatch_i]			

			if not petmatch.PetMatch_has_reached_threshold():
				continue

			user_indexes = [users.index(petmatch.lost_pet.proposed_by.user),users.index(petmatch.found_pet.proposed_by.user)]
			for user_i in user_indexes:
				#Get Lost/Found pet user
				petmatch = PetMatch.objects.get(pk=petmatch.id)
				user = users[user_i]
				password = passwords[user_i]

				#Log in First
				loggedin = client.login(username = user.username, password = password)
				self.assertTrue(loggedin == True)			
				print "[INFO]:%s logs onto %s to enter the verification page..." % (user, client)
				
				print 'petmatch users: %s, %s ' % (str(petmatch.lost_pet.proposed_by.user),str(petmatch.found_pet.proposed_by.user))

				verification_page_url = URL_VERIFY_PETMATCH + str(petmatch.id) + "/"
				print verification_page_url
				response = client.get(verification_page_url)

				userprofile = user.get_profile()

				self.assertEquals(response.status_code,200)
				message = random.choice(['yes','no'])
				post = {'message':message}
				old_lost_pet_vote = petmatch.verification_votes[0]
				response = client.post(verification_page_url,post,follow = True)
				self.assertEquals(response.status_code,200)
				petmatch = PetMatch.objects.get(pk=petmatch.id)
				new_lost_pet_vote  = petmatch.verification_votes[0]
				if old_lost_pet_vote == '0':
					sent_vote = '1' if (message == 'yes') else '2'if (message == 'no') else '0'
					self.assertEquals(sent_vote,new_lost_pet_vote)
				else:
					self.assertEquals(old_lost_pet_vote,new_lost_pet_vote)
				
				
	def test_function_PetMatch_has_reached_threshold(self):
		print_testing_name("test_function_PetMatch_has_reached_threshold")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			#indexes
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petmatch_i = random.randrange(0, NUMBER_OF_TESTS/2)	
			#objects
			client = clients [client_i]
			petmatch = petmatches [petmatch_i]			
			'''if PetMatch_has_reached_threshold() returns true, 
			the PetMatch should satisfy the threshold condition'''
			if petmatch.PetMatch_has_reached_threshold():
				self.assertTrue(petmatch.up_votes.count() - petmatch.down_votes.count() >= 5)
			else:
				self.assertTrue(petmatch.up_votes.count() - petmatch.down_votes.count() < 5)
			print 'Pet Match %s passed the test: test_function_PetMatch_has_reached_threshold' % (str(petmatch))

	def test_function_verify_PetMatch(self):
		print_testing_name("test_function_verify_PetMatch")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			#indexes
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petmatch_i = random.randrange(0, NUMBER_OF_TESTS/2)	
			#objects
			client = clients [client_i]
			petmatch = PetMatch.objects.get(pk = petmatches[petmatch_i].id)
			print 'PetMatch threshold reached: %s ' %(str(petmatch.PetMatch_has_reached_threshold()))
			print 'PetMatch is_open: %s verification_triggered: %s' % (str(petmatch.is_open),str(petmatch.verification_triggered))
			if petmatch.PetMatch_has_reached_threshold() is True:	
				self.assertFalse(petmatch.is_open)
				self.assertTrue(petmatch.verification_triggered)
	    	else:
	    		self.assertFalse(petmatch.is_successful)
	    		# self.assertFalse(petmatch.verification_triggered)
		print 'Pet Match has passed the test: test_function_verify_PetMatch'

	def test_function_close_PetMatch(self):
		print_testing_name("test_function_close_PetMatch")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords
		(users, passwords, clients, petreports, petmatches) = create_test_view_setup(create_petreports=True, create_petmatches=True)
		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			#indexes
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petmatch_i = random.randrange(0, NUMBER_OF_TESTS/2)	
			#objects
			client = clients [client_i]
			petmatch = petmatches [petmatch_i]		
			verification_page_url = URL_VERIFY_PETMATCH + str(petmatch.id) + "/"
			if petmatch.PetMatch_has_reached_threshold():
					self.assertTrue(petmatch.verification_triggered)
					self.assertFalse(petmatch.is_open)
					user_indexes = [users.index(petmatch.lost_pet.proposed_by.user),users.index(petmatch.found_pet.proposed_by.user)]
					old_pet_vote = petmatch.verification_votes
					for user_i in user_indexes:
						petmatch = PetMatch.objects.get(pk=petmatch.id)
						user = users[user_i]
						password = passwords[user_i]
						#Log in First
						loggedin = client.login(username = user.username, password = password)
						self.assertTrue(loggedin == True)			
						print "[INFO]:%s logs onto %s to enter the verification page..." % (user, client)
						user_response = random.randint(1,2)
						message = random.choice(['yes','no'])
						post = {'message':message}
						response = client.post(verification_page_url,post,follow = True)
						self.assertEquals(response.status_code,200)
						petmatch = PetMatch.objects.get(pk=petmatch.id)					
					petmatch = PetMatch.objects.get(pk=petmatch.id)
					new_pet_vote  = petmatch.verification_votes
					self.assertTrue(petmatch.closed_date != None)
					if new_pet_vote == '11':
						self.assertTrue(petmatch.is_successful)
						for pm in petmatch.lost_pet.lost_pet_related.all(): 
							self.assertFalse(pm.is_open)
							self.assertTrue(pm.closed_date != None)
						for pm in petmatch.found_pet.found_pet_related.all(): 
							self.assertFalse(pm.is_open)
							self.assertTrue(pm.closed_date != None)
					else:
						self.assertFalse(petmatch.is_successful)
			print 'Pet Match has passed the test: test_function_verify_PetMatch'