from project.settings import MEDIA_ROOT

VERIFICATION_DEFAULT_THRESHOLD = 5

#HTML
HTML_VERIFY_PETMATCHCHECK = "verifying/verify_petmatchcheck.html"
HTML_PETREUNION_FORM = "verifying/petreunion_form.html"
HTML_PETREUNION = "verifying/petreunion.html"

#URLs
URL_PETREUNION = "/verifying/"
URL_GET_PETREUNIONS_JSON = "/verifying/get_PetReunions_JSON"
URL_VERIFY_PETMATCHCHECK = "/verifying/check_PetMatch/"
URL_PETREUNION_FORM = "/reporting/close/"

NUM_PETREUNIONS_HOMEPAGE = 25

#Email Constants
EMAIL_SUBJECT_VERIFY_PETMATCH = "EmergencyPetMatcher (EPM): We have found a potential match for your pet!"
TEXTFILE_EMAIL_MATCHER_VERIFY_PETMATCH = "verifying/verification_email_to_pet_matcher_contact.txt"
TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH = "verifying/verification_email_to_pet_original_contact.txt"
TEXTFILE_EMAIL_CROSSPOSTER_VERIFY_PETMATCH = "verifying/verification_email_to_pet_crosspost_contact.txt"
TEXTFILE_EMAIL_CLOSE_PETREPORT_SUBJECT = "EmergencyPetMatcher: Please Close Your Pet Report!"
TEXTFILE_EMAIL_CLOSE_PETREPORT_BODY = "verifying/close_petreport.txt"

PETREUNION_MEDIA_DIRECTORY = MEDIA_ROOT + "petreunion/"
PETREUNION_THUMBNAILS_DIRECTORY = PETREUNION_MEDIA_DIRECTORY + "thumbnails/"
PETREUNION_UPLOADS_DIRECTORY = PETREUNION_MEDIA_DIRECTORY + "uploads/"

PETREUNION_LOCATION_LENGTH = 100
PETREUNION_DESCRIPTION_LENGTH = 500
PETREUNION_REASON_LENGTH = 200
PETREUNION_IMG_PATH = "petreunion/uploads/"
PETREUNION_THUMB_PATH = "petreunion/thumbnails/"

#PetReport Image constants
PETREUNION_THUMBNAIL_WIDTH = 128
PETREUNION_THUMBNAIL_HEIGHT = 128
