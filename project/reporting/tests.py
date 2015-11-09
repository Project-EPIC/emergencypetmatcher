from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from django.test import TestCase
from utilities.utils import *
from fixture import *
from socializing.models import UserProfile
from pprint import pprint
import unittest, string, random, sys, time, project.settings, pdb

class PetReportTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_save_petreport(self):
		user, password = create_random_User()
		pr = create_random_PetReport(user=user)
		pet_report = PetReport.objects.get(proposed_by__user=user)
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

	def test_update_petreport(self):
		user, password = create_random_User()
		pr = create_random_PetReport(user=user)
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
		pet_report = PetReport.objects.get(proposed_by = user.userprofile)
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

	def test_delete_petreport(self):
		user, password = create_random_User(0)
		pr = create_random_PetReport(user=user)
		PetReport.objects.get(proposed_by__user=user).delete()
		self.assertTrue(len(PetReport.objects.all()) == 0)

	def test_close_petreport(self):
		user, pwd = create_random_User()
		pr = create_random_PetReport(user=user)
		petreunion = PetReunion.objects.create(petreport=pr, reason="Reunited with its owner")
		pr = PetReport.objects.get(pk=pr.id)
		self.assertTrue(pr.closed == True)
		self.assertEquals(pr.id, petreunion.petreport.id)


class ReportingTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_post_petreport_success(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		response = client.get(URL_PETREPORT_FORM)
		self.assertTrue(response.status_code == 200)
		self.assertTrue(response.request['PATH_INFO'] == URL_PETREPORT_FORM)
		#Create and submit a Pet Report object as form content
		pr = create_random_PetReport(user=user, save=False)
		pr_dict = model_to_dict(pr)
		pr_dict ['img_path'] = None #Nullify the img_path attribute
		form  = PetReportForm() #Create an unbound form
		settings.RECAPTCHA_SERVER_SECRET=settings.TEST_RECAPTCHA_SERVER_SECRET
		post = {'form': form, "g-recaptcha-response":settings.TEST_RECAPTCHA_CLIENT_SECRET}
		post.update(pr_dict)
		response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)

		#Make the POST request Call
		response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(len(response.redirect_chain) == 1)
		self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
		self.assertEquals(response.redirect_chain[0][1], 302)
		self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)

	def test_post_petreport_fail(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		response = client.get(URL_PETREPORT_FORM)
		self.assertTrue(response.status_code == 200)
		self.assertTrue(response.request['PATH_INFO'] == URL_PETREPORT_FORM)
		#Create and submit a Pet Report object as form content
		pr = create_random_PetReport(user=user, save=False)
		pr_dict = model_to_dict(pr)
		pr_dict ['img_path'] = None #Nullify the img_path attribute

		#Generate bad input
		pr_dict ['sex'] = generate_string(5)
		pr_dict ['size'] = generate_string(10)
		pr_dict ['status'] = generate_string(5)
		pr_dict ['date_lost_or_found'] = 100

		form  = PetReportForm() #Create an unbound form
		settings.RECAPTCHA_SERVER_SECRET=settings.TEST_RECAPTCHA_SERVER_SECRET
		post = {'form': form, "g-recaptcha-response":settings.TEST_RECAPTCHA_CLIENT_SECRET}
		post.update(pr_dict)
		response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)

		#Make the POST request Call
		response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.request ['PATH_INFO'] == URL_PETREPORT_FORM)
		self.assertTrue(len(PetReport.objects.all()) == 0)

	def test_add_petreport_bookmark(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		petreport = create_random_PetReport(user=user)
		loggedin = client.login(username = user.username, password = pwd)
		post =  {"petreport_id":petreport.id, "action":"Bookmark this Pet"}
		response = client.post(URL_BOOKMARK_PETREPORT, post, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ['PATH_INFO'], URL_BOOKMARK_PETREPORT)
		self.assertTrue(petreport.UserProfile_has_bookmarked(user.userprofile))
		self.assertEquals(petreport.bookmarked_by.get(pk=user.id), user.userprofile)

	def test_remove_petreport_bookmark(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		petreport = create_random_PetReport(user=user)
		loggedin = client.login(username = user.username, password = pwd)
		user.userprofile.bookmarks_related.add(petreport)
		post =  {"petreport_id":petreport.id, "action":"Remove Bookmark"}
		response = client.post(URL_BOOKMARK_PETREPORT, post, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ['PATH_INFO'], URL_BOOKMARK_PETREPORT)
		self.assertFalse(petreport.UserProfile_has_bookmarked(user.userprofile))

	def test_close_petreport_success(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		petreport = create_random_PetReport(user=user)
		loggedin = client.login(username=user.username, password=pwd)
		response = client.get(URL_CLOSE_PETREPORT + "%d/" % petreport.id)
		self.assertEquals(response.status_code, 200)
		post = model_to_dict(create_random_PetReunion(save=False, petreport=petreport))
		settings.RECAPTCHA_SERVER_SECRET=settings.TEST_RECAPTCHA_SERVER_SECRET
		post["g-recaptcha-response"] = settings.TEST_RECAPTCHA_CLIENT_SECRET
		response = client.post(URL_CLOSE_PETREPORT + "%d/" % petreport.id, post, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ["PATH_INFO"], URL_HOME)
		self.assertTrue(PetReunion.objects.filter(petreport=petreport).exists())

	def test_close_petreport_fail(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		petreport = create_random_PetReport(user=user)
		loggedin = client.login(username=user.username, password=pwd)
		post = model_to_dict(create_random_PetReunion(save=False, petreport=petreport))
		post["reason"] = 10000
		post["description"] = generate_string(PETREUNION_DESCRIPTION_LENGTH + 1000)
		settings.RECAPTCHA_SERVER_SECRET=settings.TEST_RECAPTCHA_SERVER_SECRET
		post["g-recaptcha-response"] = settings.TEST_RECAPTCHA_CLIENT_SECRET
		response = client.post(URL_CLOSE_PETREPORT + "%d/" % petreport.id, post, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ["PATH_INFO"], URL_CLOSE_PETREPORT + "%d/" % petreport.id)
		self.assertFalse(PetReunion.objects.filter(petreport=petreport).exists())
