from project.settings import NOSQL_DATABASES
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import logger
from constants import *

'''===================================================================================
[documenter.py]: NoSQL layer for retrieving and inserting data into the EPM NoSQL Database.
==================================================================================='''


''' ============================ [CONNECTION] ==================================== '''
#Setup connection and connection parameters
try:
	#Note that the max_pool_size parameter does not indicate that only x connection 
	#threads can be executed simultaneously but that the MongoClient keeps x *idle* threads in the pool.
	HOST = NOSQL_DATABASES ["mongodb"]["HOST"]
	PORT = NOSQL_DATABASES ["mongodb"]["PORT"]
	MAX_POOL_SIZE = NOSQL_DATABASES ["mongodb"]["MAX_POOL_SIZE"]
	connection = MongoClient(host=HOST, port=PORT, max_pool_size=MAX_POOL_SIZE)
	print "[OK]: The MongoDB instance is running at [%s] and port [%d].\n" % (HOST, PORT)

except ConnectionFailure as cf:
	print "[ERROR]: %s \n\tCannot connect to the MongoDB instance at host [%s] and port [%d]. Is your MongoDB server (mongod) running?\n" % (cf, HOST, PORT)

try:
	TEST_HOST = NOSQL_DATABASES ["mongodb_test"]["HOST"]
	TEST_PORT = NOSQL_DATABASES ["mongodb_test"]["PORT"]
	TEST_MAX_POOL_SIZE = NOSQL_DATABASES ["mongodb_test"]["MAX_POOL_SIZE"]
	test_connection = MongoClient(host=TEST_HOST, port=TEST_PORT, max_pool_size=TEST_MAX_POOL_SIZE)
	print "[OK]: The Test MongoDB instance is running at [%s] and port [%d].\n" % (TEST_HOST, TEST_PORT)

except ConnectionFailure as cf:
	print "[ERROR]: %s \n\tCannot connect to the Test MongoDB instance at host [%s] and port [%d]. Is your MongoDB server (mongod) running?\n" % (cf, TEST_HOST, TEST_PORT)


''' ============================ [FUNCTIONS] ==================================== '''

def get_mongo_database_connection(is_test=True):
	if (is_test == True):
		return test_connection [NOSQL_DATABASES["mongodb_test"]["NAME"]]
	return connection [NOSQL_DATABASES ["mongodb"]["NAME"]]

def query(collection_name, dictionary, is_test=True, for_one_result=True):
	db = get_mongo_database_connection(is_test)
	collection = db [collection_name]

	#One result or many?
	if for_one_result == True:
		result = collection.find_one(dictionary)
	else:
		result = collection.find(dictionary)
	return result

def insert(collection_name, dictionary, is_test=True):
	db = get_mongo_database_connection(is_test)
	collection = db [collection_name]

	try:
		collection.insert(dictionary)
	except OperationFailure as of:
		print "[ERROR]: %s \n\tCannot insert document to MongoDB instance." % (of)
	return True
	
#Drop all collections in the specified database.
def empty_collections (is_test=True):
	db = get_mongo_database_connection(is_test)
	for collection in db.collection_names():
		if collection == "system.indexes": 
			continue
		db[collection].drop()
	return True

#Given a userprofile ID and date object, retrieve activities in "UserProfile_activities" collection
#that satisfy the predicates.
def get_UserProfile_activities(userprofile_id, date_last_logged_in, is_test=True, for_one_result=True):
	if isinstance (date_last_logged_in, datetime.date):
		date_last_logged_in = datetime.strptime(date_last_logged_in)

	#Build the query.
	collection_query = {}
	collection_query [DOCUMENT_USERPROFILE_ID] = userprofile_id
	collection_query [DOCUMENT_TIMESTAMP] = date_last_logged_in
	#Now, call the query function to take care of the querying.
	return query(COLLECTION_USERPROFILE_ACTIVITIES, collection_query, is_test=is_test, for_one_result=for_one_result)

#Given a petreport ID and date object, retrieve activities in "PetReport_activities" collection
#that satisfy the predicates.
def get_PetReport_activities(petreport_id, date_last_logged_in, is_test=True):
	#Build the query.
	collection_query = {}
	collection_query [DOCUMENT_PETREPORT_ID] = petreport_id
	collection_query [DOCUMENT_TIMESTAMP] = date_last_logged_in
	#Now, call the query function to take care of the querying.
	return query(COLLECTION_PETREPORT_ACTIVITIES, collection_query, is_test=is_test, for_one_result=for_one_result)

#Given a petmatch ID and date object, retrieve activities in "PetMatch_activities" collection
#that satisfy the predicates.
def get_PetMatch_activities(petmatch_id, date_last_logged_in, is_test=True):
	#Build the query.
	collection_query = {}
	collection_query [DOCUMENT_PETMATCH_ID] = petmatch_id
	collection_query [DOCUMENT_TIMESTAMP] = date_last_logged_in
	#Now, call the query function to take care of the querying.
	return query(COLLECTION_PETMATCH_ACTIVITIES, collection_query, is_test=is_test, for_one_result=for_one_result)

def insert_activity():
	pass
















