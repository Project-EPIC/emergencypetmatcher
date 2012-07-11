from home.models import *
from django.contrib.auth import authenticate
from django.test.client import Client
import unittest, string, random, sys, time
import test_utils as utils

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
ReportingTesting: Testing for EPM Pet Reporting
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class ReportingTesting (unittest.TestCase):

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

	def test_createPetReport(self):
		print '>>>> Testing test_createPetReport for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		clients = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		users = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		passwords = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		user_count = 0
		client_count = 0

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			user = users [user_i]
			client = clients [client_i]

			if user is None:
				user, password = utils.create_random_User(i, pretty_name=True)
				users [user_i] = user
				passwords [user_i] = password
				user_count += 1

			if client is None:
				client = Client (enforce_csrf_checks=False)
				clients [client_i] = client
				client_count += 1

			print "\n%s logs onto %s to create a pet report..." % (user, client)

			loggedin = client.login(username = users [user_i].username, password = passwords[user_i])
			self.assertTrue(loggedin == True)
			response = client.get('/reporting/submit_petreport')
			self.assertTrue(response.status_code == 200)
			#We should have the base.html -> index.html -> petreport_form.html
			self.assertTrue(len(response.templates) == 3)

			pr = utils.create_random_PetReport(user)
			form = PetReportForm(instance = pr)
			response = client.post('/reporting/submit_petreport', {'form':form})
			client.logout()

			self.assertTrue(response.status_code == 200)			
			self.assertTrue(len(User.objects.all()) == user_count)
			self.assertTrue(len(UserProfile.objects.all()) == user_count)
			self.assertTrue(len(PetReport.objects.all()) == i + 1)
			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= utils.NUMBER_OF_TESTS and user_count <= utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(User.objects.all()) <= utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)













































