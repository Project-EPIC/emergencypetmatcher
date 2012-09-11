from home.models import *
from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
import unittest, string, random, sys, time
import utils

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

	def test_get_petreport_form(self):
		print '>>>> Testing test_get_petreport_form for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients) = utils.create_test_view_setup(create_petreports=False)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "\n%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(utils.TEST_SUBMIT_PETREPORT_URL)
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request ['PATH_INFO'] == utils.TEST_SUBMIT_PETREPORT_URL)
			#We should have the base.html -> index.html -> petreport_form.html
			self.assertTrue(len(response.templates) == 3)

			client.logout()

			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		utils.performance_report(iteration_time)


	def test_post_good_PetReport(self):
		print '>>>> Testing test_post_good_PetReport for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients) = utils.create_test_view_setup(create_petreports=False)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "\n%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(utils.TEST_SUBMIT_PETREPORT_URL)

			#Create and submit a Pet Report object as form content
			pr = utils.create_random_PetReport(users [user_i])

			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			pr_dict = model_to_dict(pr) 
			pr_dict ['img_path'] = None #Nullify the img_path attribute
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)

			#Make the POST request Call
			response = client.post(utils.TEST_SUBMIT_PETREPORT_URL, post, follow=True)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			# self.assertTrue(len(response.redirect_chain) == 1) UNCOMMENT ONCE RESOLVED
			# self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/') UNCOMMENT ONCE RESOLVED
			# self.assertEquals(response.redirect_chain[0][1], 302) UNCOMMENT ONCE RESOLVED
			# self.assertTrue(response.request ['PATH_INFO'] == utils.TEST_HOME_URL) UNCOMMENT ONCE RESOLVED
			# self.assertTrue(len(PetReport.objects.all()) == 2*i + 2) UNCOMMENT ONCE RESOLVED
			client.logout()

			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= utils.NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= utils.NUMBER_OF_TESTS)	
		# self.assertTrue(len(PetReport.objects.all()) == 2*utils.NUMBER_OF_TESTS) UNCOMMENT ONCE RESOLVED
		utils.performance_report(iteration_time)


	def test_post_bad_PetReport(self):
		print '>>>> Testing test_post_bad_PetReport for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients) = utils.create_test_view_setup(create_petreports=False)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "\n%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(utils.TEST_SUBMIT_PETREPORT_URL)

			#Create and submit a Pet Report object as form content
			pr = utils.create_random_PetReport(users [user_i])
			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			pr_dict = model_to_dict(pr)

			#Generate bad input
			if i %2 == 0:
				pr_dict ['sex'] = utils.generate_string(5)
			elif i%3 == 0:
				pr_dict ['size'] = utils.generate_string(10)
			elif i%5 == 0:
				pr_dict ['status'] = utils.generate_string(5)
			else:
				pr_dict ['date_lost_or_found'] = 100

			pr_dict ['img_path'] = None #Nullify the img_path attribute
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)

			#Make the POST request Call
			response = client.post(utils.TEST_SUBMIT_PETREPORT_URL, post, follow=True)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertTrue(response.request ['PATH_INFO'] == utils.TEST_SUBMIT_PETREPORT_URL)
			self.assertTrue(len(PetReport.objects.all()) == i + 1)
			client.logout()

			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= utils.NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)

	def test_get_PetReport_detailed_page(self):
		print '>>>> Testing test_get_PetReport_detailedpage for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords and petreports 
		(users, passwords, clients, petreports) = utils.create_test_view_setup(create_petreports=True)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]
			prdp_url = utils.TEST_PRDP_URL + str(petreport.id) + "/"

			#Test without logging in First.
			print "\n\nGetting PRDP from %s without being logged in" % (client)
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertTrue(response.request ['PATH_INFO'] == prdp_url)

			#Log in
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "%s logs onto %s to EPM" % (user, client)

			#Test after Logging in.
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertTrue(response.request ['PATH_INFO'] == prdp_url)

			#Test navigation to user profiles of all workers
			for worker in petreport.workers.all():
				worker_url = utils.TEST_USERPROFILE_URL +str(worker.user.id)+ "/"
				response = client.get(worker_url)
				self.assertEquals(response.status_code, 200)
				self.assertTrue(response.request ['PATH_INFO'] == worker_url)

			print "Navigation to all workers' user profiles is successful"

			#Test navigation to the matching interface
			matching_url = utils.TEST_MATCHING_URL + str(petreport.id) + "/"
			print 'matching url: '+matching_url
			response = client.get(matching_url)
			# self.assertEquals(response.status_code, 200) UNCOMMENT ONCE RESOLVED
			self.assertTrue(response.request ['PATH_INFO'] == matching_url)

			print "Navigation to the matching interface is successful"

			#test navigation to the PMDP
			client.logout()

			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		utils.performance_report(iteration_time)

	def test_add_PetReport_bookmark(self):
		print '>>>> Testing test_add_PetReport_bookmark for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate bookmarking of PetReport objects.
		(users, passwords, clients, petreports) = utils.create_test_view_setup(create_petreports=True)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "\n%s logs onto %s to enter the PRDP..." % (user, client)

			prdp_url = utils.TEST_PRDP_URL + str(petreport.id) + "/"
			print prdp_url
			response = client.get(prdp_url)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			add_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], add_bookmark_url)
			self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()))
			self.assertEquals(petreport.bookmarked_by.get(pk = user.id), user.get_profile())
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count-1))

			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		utils.performance_report(iteration_time)	

	def test_remove_petreport_bookmark(self):
		print '>>>> Testing test_add_PetReport_bookmark for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate bookmarking of PetReport objects.
		(users, passwords, clients, petreports) = utils.create_test_view_setup(create_petreports=True)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "\n%s logs onto %s to enter the PRDP..." % (user, client)

			#navigate to the prdp
			prdp_url = utils.TEST_PRDP_URL + str(petreport.id) + "/"
			print prdp_url
			response = client.get(prdp_url)


			#add a bookmark
			add_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			#remove the bookmark
			remove_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Remove Bookmark"}
			response = client.post(remove_bookmark_url, post, follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], remove_bookmark_url)
			#self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()),False)
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))

			#add back the bookmark
			add_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()


			#navigate to the bookmarks page
			bookmarks_page_url = utils.TEST_BOOKMARKED_PETREPORTS_URL
			print bookmarks_page_url
			response = client.get(bookmarks_page_url)

			#remove the bookmark 
			remove_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Remove Bookmark"}
			response = client.post(add_bookmark_url, post, follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()


			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], remove_bookmark_url)
			#self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()),False)
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))


			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''

		utils.performance_report(iteration_time)	

	def test_get_bookmarks_page(self):
		print '>>>> Testing test_get_bookmarks_page for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate retrieving the bookmarks page for a user.
		(users, passwords, clients, petreports) = utils.create_test_view_setup(create_petreports=True)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print "\n%s logs onto %s to enter the bookmarks page..." % (user, client)

			#navigate to the bookmarks page
			bookmarks_page_url = utils.TEST_BOOKMARKED_PETREPORTS_URL
			print bookmarks_page_url
			response = client.get(bookmarks_page_url)




