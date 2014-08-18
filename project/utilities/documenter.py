from project.settings import NOSQL_DATABASES
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from home.constants import *
from utilities.utils import print_debug_msg
from datetime import datetime

#Setup connection and connection parameters
try:
	#Note that the max_pool_size parameter does not indicate that only x connection 
	#threads can be executed simultaneously but that the MongoClient keeps x *idle* threads in the pool.
	HOST = NOSQL_DATABASES ["mongodb"]["HOST"]
	MAX_POOL_SIZE = NOSQL_DATABASES ["mongodb"]["MAX_POOL_SIZE"]
	connection = MongoClient(host=HOST, max_pool_size=MAX_POOL_SIZE)
	print "[OK]: The MongoDB instance is running at [%s].\n" % (HOST)

except ConnectionFailure as cf:
	print "[ERROR]: %s \n\tCannot connect to the MongoDB instance at host [%s]. Is your MongoDB server (mongod) running?\n" % (cf, HOST)


def get_mongo_database_connection():
	return connection [NOSQL_DATABASES ["mongodb"]["NAME"]]

def build_collection_query (userprofile_id, since_date, activity=None):
	collection_query = { DOCUMENTER_KEY_USERPROFILE_ID: userprofile_id, DOCUMENTER_KEY_DATE: since_date }

	if activity != None:
		collection_query[DOCUMENTER_KEY_ACTIVITY] = activity

	return collection_query

def query(collection_name, collection_query, limit=10, for_one_result=True):
	db = get_mongo_database_connection()
	collection = db[collection_name]

	if for_one_result == True:
		cursor = collection.find_one(collection_query)
	else:
		cursor = collection.find(collection_query).sort(DOCUMENTER_KEY_DATE)
	return cursor

def insert(collection_name, activity):
	db = get_mongo_database_connection()
	collection = db [collection_name]

	try:
		collection.insert(activity)
	except OperationFailure as of:
		print "[ERROR]: %s \n\tCannot insert document to MongoDB instance." % (of)
	return True		

def get_activities_for_feed(userprofile_id, since_date, limit=10):
	try:
		collection_query = build_collection_query(userprofile_id, since_date)
		userprofile_cursor = get_UserProfile_activities(collection_query, for_one_result=False)
		petreport_cursor = get_PetReport_activities(collection_query, for_one_result=False)
		petmatch_cursor = get_PetMatch_activities(collection_query, for_one_result=False)
		petcheck_cursor = get_PetCheck_activities(collection_query, for_one_result=False)
	except Exception as e:
		print "[ERROR]: Problem when reading from Mongo: %s" % e

	total_activities = []
	for u in userprofile_cursor:
		total_activities += u
	for pr in petreport_cursor:
		total_activities += pr
	for pm in petmatch_cursor:
		total_activities += pm

	print total_activities

	#Total # activities must be less than or equal to specified limit.
	total_activities = sorted(total_activities, key= lambda s: s[DOCUMENTER_KEY_DATE])
	# print total_activities
	return total_activities

def insert_into_UserProfiles (activity):
	insert(DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE, activity)
def insert_into_PetReports (activity):
	insert(DOCUMENTER_ACTIVITY_COLLECTION_PETREPORT, activity)
def insert_into_PetMatches (activity):
	insert(DOCUMENTER_ACTIVITY_COLLECTION_PETMATCH, activity)	
def insert_into_PetChecks (activity):
	insert(DOCUMENTER_ACTIVITY_COLLECTION_PETCHECK, activity)

def get_UserProfile_activities(collection_query, for_one_result=True):
	return query(DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE, collection_query, for_one_result=for_one_result)
def get_PetReport_activities(collection_query, for_one_result=True):
	return query(DOCUMENTER_ACTIVITY_COLLECTION_PETREPORT, collection_query, for_one_result=for_one_result)
def get_PetMatch_activities(collection_query, for_one_result=True):
	return query(DOCUMENTER_ACTIVITY_COLLECTION_PETMATCH, collection_query, for_one_result=for_one_result)
def get_PetCheck_activities(collection_query, for_one_result=True):
	return query(DOCUMENTER_ACTIVITY_COLLECTION_PETCHECK, collection_query, for_one_result=for_one_result)	

#Drop all collections in the specified database.
def empty_collections ():
	db = get_mongo_database_connection()
	for collection in db.collection_names():
		if collection != "system.indexes":
			db[collection].drop()
	return True













