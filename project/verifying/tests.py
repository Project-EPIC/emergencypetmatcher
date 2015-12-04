from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from utilities.utils import *
from fixture import *
from pprint import pprint
from django.contrib.messages import constants as messages
from django.test import TestCase
import unittest, string, random, sys, time, ipdb

class VerificationTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_get_verification_page_success (self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		pr1 = create_random_PetReport(user=user, status="Lost")
		pr2 = create_random_PetReport(user=user2, status="Found")
		pm = PetMatch.objects.create(proposed_by=user.userprofile, lost_pet=pr1, found_pet=pr2)
		pmc = PetMatchCheck.objects.create(petmatch=pm)
		loggedin = client.login(username=user.username, password=pwd)
		response = client.get(URL_VERIFY_PETMATCHCHECK + "%d/" % pmc.id, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_VERIFY_PETMATCHCHECK + "%d/" % pmc.id)

	def test_get_verification_page_fail (self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		user3, pwd3 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		pr1 = create_random_PetReport(user=user, status="Lost")
		pr2 = create_random_PetReport(user=user2, status="Found")
		pm = PetMatch.objects.create(proposed_by=user.userprofile, lost_pet=pr1, found_pet=pr2)
		pmc = PetMatchCheck.objects.create(petmatch=pm)
		loggedin = client.login(username=user3.username, password=pwd3)
		response = client.get(URL_VERIFY_PETMATCHCHECK + "%d/" % pmc.id, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_HOME)

	def test_post_verification_success(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		pr1 = create_random_PetReport(user=user, status="Lost")
		pr2 = create_random_PetReport(user=user2, status="Found")
		pm = PetMatch.objects.create(proposed_by=user.userprofile, lost_pet=pr1, found_pet=pr2)
		pmc = PetMatchCheck.objects.create(petmatch=pm)

		loggedin = client.login(username=user.username, password=pwd)
		response = client.post(URL_VERIFY_PETMATCHCHECK + "%d/" % pmc.id, {'verify-choice':'1'}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_HOME)

		loggedin = client.login(username=user2.username, password=pwd2)
		response = client.post(URL_VERIFY_PETMATCHCHECK + "%d/" % pmc.id, {'verify-choice':'1'}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_HOME)

		pm = PetMatch.objects.get(pk=pm.id)
		self.assertTrue(pm.is_successful() == True)

	def test_post_verification_fail(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		pr1 = create_random_PetReport(user=user, status="Lost")
		pr2 = create_random_PetReport(user=user2, status="Found")
		pm = PetMatch.objects.create(proposed_by=user.userprofile, lost_pet=pr1, found_pet=pr2)
		pmc = PetMatchCheck.objects.create(petmatch=pm)

		loggedin = client.login(username=user.username, password=pwd)
		response = client.post(URL_VERIFY_PETMATCHCHECK + "%d/" % pmc.id, {'verify-choice':'0'}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_HOME)

		loggedin = client.login(username=user2.username, password=pwd2)
		response = client.post(URL_VERIFY_PETMATCHCHECK + "%d/" % pmc.id, {'verify-choice':'1'}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_HOME)

		pm = PetMatch.objects.get(pk=pm.id)
		self.assertTrue(pm.is_successful() == False)

	def test_get_petreunion(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		user3, pwd3 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username=user3.username, password=pwd3)
		pr1 = create_random_PetReport(user=user, status="Lost")
		pr2 = create_random_PetReport(user=user2, status="Found")
		petreunion = create_random_PetReunion(petreport=pr1, matched_petreport=pr2)
		response = client.get(URL_PETREUNION + "%d/" % petreunion.id)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_PETREUNION + "%d/" % petreunion.id)
