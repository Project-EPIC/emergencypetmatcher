from django.contrib.auth import authenticate
from django.test.client import Client
from time import sleep
from selenium import webdriver
from pprint import pprint
from fixture import *
from django.test import TestCase
from django.template.loader import render_to_string
from project.settings import TEST_TWITTER_USER, TEST_TWITTER_PASSWORD, TEST_FACEBOOK_USER, TEST_FACEBOOK_PASSWORD, TEST_DOMAIN, EMAIL_FILE_PATH, EMAIL_BACKEND
from home.constants import *
from utilities.utils import *
import unittest, string, random, sys, time, urlparse, project.settings, math, pdb

class UserProfileTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_get_userprofile_page(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		response = client.get(URL_USERPROFILE + "%d/" % user.userprofile.id)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_USERPROFILE + "%d/" % user.userprofile.id)

	def test_message_userprofile_success(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		response = client.get(URL_USERPROFILE + "%d/" % user2.userprofile.id)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_USERPROFILE + "%d/" % user2.userprofile.id)
		response = client.post(URL_SEND_MESSAGE_TO_USER, {"target_userprofile_id": user2.userprofile.id, "message": generate_string(USERPROFILE_MESSAGE_LENGTH)}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_USERPROFILE + "%d/" % user2.userprofile.id)

	def test_message_userprofile_fail(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		response = client.post(URL_SEND_MESSAGE_TO_USER, {"target_userprofile_id": user2.userprofile.id, "message": generate_string(USERPROFILE_MESSAGE_LENGTH + 1000)}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_USERPROFILE + "%d/" % user2.userprofile.id)
		self.assertTrue("Message size is too big. Please try again." in response._container[0])

	def test_follow_success(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		response = client.post(URL_FOLLOW, {"target_userprofile_id": user2.userprofile.id}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_USERPROFILE + "%d/" % user2.userprofile.id)

	def test_unfollow_success(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		user.userprofile.following.add(user2.userprofile)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		response = client.post(URL_UNFOLLOW, {"target_userprofile_id": user2.userprofile.id}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_USERPROFILE + "%d/" % user2.userprofile.id)

	def test_save_password(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username=user.username, password=pwd)
		response = client.post(URL_EDITUSERPROFILE_PWD, {
			"action":"savePassword",
			"old_password":pwd,
			"new_password1":"new_password",
			"new_password2":"new_password"
		}, follow=True)
		self.assertFalse(client.login(username=user.username, password=pwd))
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_EDITUSERPROFILE + "%d/" % user.userprofile.id)

	def test_save_profile(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		username = generate_string (User._meta.get_field('username').max_length)
		first_name = generate_string (User._meta.get_field('first_name').max_length)
		last_name = generate_string (User._meta.get_field('last_name').max_length)
		description = generate_string (UserProfile._meta.get_field("description").max_length)
		response = client.post(URL_EDITUSERPROFILE_INFO, {
			"action":"saveProfile",
			"username":username,
			"first_name":first_name,
			"last_name":last_name,
			"email":"test@test.com",
			"description":description
		}, follow=True)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request['PATH_INFO'], URL_USERPROFILE + "%d/" % user.userprofile.id)
