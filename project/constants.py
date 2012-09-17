'''===================================================================================
[constants.py]: Constants for the EPM system
==================================================================================='''

#Lower and Upper bounds for Lost and Found Dates
DATE_LOWER_BOUND = "2012-01-01"
DATE_UPPER_BOUND = "2012-08-16"

#Small List of Names
USERNAMES = ['Jacob', 'Emily', 'Joshua', 'Madison', 'Kenneth', 'Mark', 'Dave', 'Angela', '' 'Matthew', 'Olivia', 'Daniel', 'Hannah', 
'Chris', 'Abby', 'Andrew', 'Isabella', 'Mario', 'Sahar', 'Amrutha', 'Leysia', 'Ken', 'Abe']
PETREPORT_NAMES = ['Sparky', 'Nugget', 'Sydney', 'Missy', 'Marley', 'Fousey', 'Daisy', 'Libby', 'Apollo', 'Bentley', 'Scruffy',
'Dandy', 'Candy', 'Mark', 'Baby', 'Toodle', 'Princess' ,'Prince', 'Guss']

#Identifiers
UPVOTE = "upvote"
DOWNVOTE = "downvote"

#Activity Enum Values
ACTIVITY_LOG_DIRECTORY = "../logs/activity_logs/"
ACTIVITY_ACCOUNT_CREATED = "ACCOUNT_CREATED"
ACTIVITY_LOGIN = "LOGIN"
ACTIVITY_LOGOUT = "LOGOUT"
ACTIVITY_PETREPORT_SUBMITTED = "PETREPORT_SUBMITTED"
ACTIVITY_PETMATCH_PROPOSED = "PETMATCH_PROPOSED"
ACTIVITY_PETMATCH_UPVOTE = "PETMATCH_UPVOTE"
ACTIVITY_PETMATCH_DOWNVOTE= "PETMATCH_DOWNVOTE"

#Represents how many activities to fetch per request.
ACTIVITY_FEED_LENGTH = 25

#URLS - use for redirect calls
URL_HOME = '/'
URL_LOGIN = '/login'
URL_SUBMIT_PETREPORT ='/reporting/submit_PetReport'
URL_USERPROFILE = '/UserProfile/'
URL_PRDP = '/reporting/PetReport/'
URL_PMDP = '/matching/PetMatch/'
URL_VOTE_MATCH = '/matching/vote_PetMatch'
URL_MATCHING = "/matching/match_PetReport/"
URL_PROPOSE_MATCH = "/matching/propose_PetMatch/"
 
#HTML File Paths (relative to STATIC_URL) - use for render_to_response calls
HTML_HOME = "home/index.html"
HTML_LOGIN = "registration/login.html"
HTML_SUBMIT_PETREPORT = "reporting/petreport_form.html"
HTML_USERPROFILE = "home/userprofile.html"
HTML_PRDP = "reporting/petreport.html"
HTML_PMDP = "matching/petmatch.html"
HTML_MATCHING = "matching/matching.html"
HTML_PROPOSE_MATCH = "matching/propose_match.html"
HTML_SOCIAL_AUTH_FORM = "registration/social_auth_username_form.html"