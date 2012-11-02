import os

'''===================================================================================
[constants.py]: Constants for the EPM system
==================================================================================='''

#Number of Tests
NUMBER_OF_TESTS = 10

#Lower and Upper bounds for Lost and Found Dates
DATE_LOWER_BOUND = "2012-01-01"
DATE_UPPER_BOUND = "2012-08-16"

#max_length for Model Fields
USER_USERNAME_LENGTH = 30
USER_FIRSTNAME_LENGTH = 30
USER_LASTNAME_LENGTH = 30
USER_PASSWORD_LENGTH = 30
PETREPORT_PET_TYPE_LENGTH = 10
PETREPORT_STATUS_LENGTH = 5
PETREPORT_SEX_LENGTH = 6
PETREPORT_SIZE_LENGTH = 30
PETREPORT_LOCATION_LENGTH = 25
PETREPORT_PET_NAME_LENGTH = 15 
PETREPORT_AGE_LENGTH = 10
PETREPORT_COLOR_LENGTH =30
PETREPORT_BREED_LENGTH = 30
PETREPORT_DESCRIPTION_LENGTH = 500
PETMATCH_DESCRIPTION_LENGTH = 300
CHATLINE_TEXT_LENGTH = 10000

#Small List of Names
USERNAMES = ['Jacob', 'Emily', 'Joshua', 'Madison', 'Kenneth', 'Mark', 'Dave', 'Angela', '' 'Matthew', 'Olivia', 'Daniel', 'Hannah', 
'Chris', 'Abby', 'Andrew', 'Isabella', 'Mario', 'Sahar', 'Amrutha', 'Leysia', 'Ken', 'Abe']
PETREPORT_NAMES = ['Sparky', 'Nugget', 'Sydney', 'Missy', 'Marley', 'Fousey', 'Daisy', 'Libby', 'Apollo', 'Bentley', 'Scruffy',
'Dandy', 'Candy', 'Mark', 'Baby', 'Toodle', 'Princess' ,'Prince', 'Guss']

#Identifiers
UPVOTE = "upvote"
DOWNVOTE = "downvote"

#File Path Constants
ACTIVITY_LOG_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/logs/activity_logs/"
TEST_ACTIVITY_LOG_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/logs/test_activity_logs/"
PETREPORT_IMAGES_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/static/images/petreport_images/"
USERPROFILE_IMAGES_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/static/images/profile_images/"

#Activity Enum Values
ACTIVITY_ACCOUNT_CREATED = "ACCOUNT_CREATED"
ACTIVITY_LOGIN = "LOGIN"
ACTIVITY_LOGOUT = "LOGOUT"
ACTIVITY_PETREPORT_SUBMITTED = "PETREPORT_SUBMITTED"
ACTIVITY_PETREPORT_ADD_BOOKMARK = "PETREPORT_ADD_BOOKMARK"
ACTIVITY_PETREPORT_REMOVE_BOOKMARK = "PETREPORT_REMOVE_BOOKMARK"
ACTIVITY_PETMATCH_PROPOSED = "PETMATCH_PROPOSED"
ACTIVITY_PETMATCH_UPVOTE = "PETMATCH_UPVOTE"
ACTIVITY_PETMATCH_DOWNVOTE= "PETMATCH_DOWNVOTE"
ACTIVITY_FOLLOWING = "_FOLLOWING"
ACTIVITY_UNFOLLOWING = "UNFOLLOWING"
ACTIVITY_FOLLOWER = "_FOLLOWER"
ACTIVITY_UNFOLLOWER = "UNFOLLOWER"
ACTIVITY_PETMATCH_PROPOSED_LOST_BOOKMARKED_PETREPORT = "PETMATCH_LOST_BOOKMARKED_PETREPORT"
ACTIVITY_PETMATCH_PROPOSED_FOUND_BOOKMARKED_PETREPORT = "PETMATCH_FOUND_BOOKMARKED_PETREPORT"
ACTIVITY_USER_CHANGED_USERNAME = "USER_CHANGED_USERNAME"
ACTIVITY_USER_BEING_FOLLOWED = "USER_BEING_FOLLOWED"
ACTIVITY_USER_BEING_UNFOLLOWED = "USER_BEING_UNFOLLOWED"

#Reputation reward points
REWARD_PETMATCH_VOTE = 2
REWARD_PETREPORT_SUBMIT = 5
REWARD_PETMATCH_PROPOSE = 5
REWARD_USER_FOLLOWED = 2

#Represents how many activities to fetch per request.
ACTIVITY_FEED_LENGTH = 10


#URLS - use for redirect calls
URL_HOME = '/'
URL_GET_ACTIVITIES = "/get_activities_json"
URL_LOGIN = '/login'
URL_SUBMIT_PETREPORT ='/reporting/submit_PetReport'
URL_USERPROFILE = '/UserProfile/'
URL_PRDP = '/reporting/PetReport/'
URL_PMDP = '/matching/PetMatch/'
URL_VOTE_MATCH = '/matching/vote_PetMatch'
URL_MATCHING = "/matching/match_PetReport/"
URL_PROPOSE_MATCH = "/matching/propose_PetMatch/"
URL_BOOKMARK_PETREPORT = "/reporting/bookmark_PetReport"
URL_BOOKMARKED = "/reporting/bookmarks/"
URL_FOLLOW = "/follow/"
URL_UNFOLLOW = "/unfollow/"
URL_EDITUSERPROFILE = "/edituserprofile/"
URL_EMAIL_VERIFICATION_COMPLETE = "/email_verification_complete/" 

#HTML File Paths (relative to STATIC_URL) - use for render_to_response calls
HTML_HOME = "home/index.html"
HTML_LOGIN = "registration/login.html"
HTML_SUBMIT_PETREPORT = "reporting/petreport_form.html"
HTML_USERPROFILE = "home/userprofile.html"
HTML_PRDP = "reporting/petreport.html"
HTML_PMDP = "matching/petmatch.html"
HTML_MATCHING = "matching/matching.html"
HTML_PROPOSE_MATCH = "matching/propose_match.html"
HTML_SOCIAL_AUTH_FORM = "registration/social_auth_form.html"
HTML_EDITUSERPROFILE_FORM ="home/EditUserProfile_form.html"
TEXTFILE_EMAIL_ACTIVATION_SUBJECT="registration/activation_email_subject.txt"
TEXTFILE_EMAIL_CHANGE_VERICATION="home/email_change_verification.txt"
TEST_EMAIL="emergencypetmatchertest@gmail.com"
