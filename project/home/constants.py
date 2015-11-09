import os
from project.settings import STATIC_URL

#URLS - use for redirect calls
URL_HOME = '/'
URL_GET_ACTIVITIES_JSON = "/get_activities"
URL_GET_BOOKMARKS_JSON = "/get_bookmarks"
URL_LOGIN = '/login'
URL_LOGOUT = '/logout'
URL_REGISTRATION = "/accounts/register/"
URL_REGISTRATION_COMPLETE = "/register/complete/"
URL_ACTIVATION_COMPLETE = "/accounts/activate/complete/"
URL_SOCIAL_AUTH_GET_DETAILS = "/social_auth_get_details"
URL_SOCIAL_AUTH_COMPLETE = "/complete/"

#HTML File Paths (relative to STATIC_URL) - use for render_to_response calls
HTML_HOME = "home/index.html"
HTML_ABOUT = "home/about.html"
HTML_404 = "home/404.html"
HTML_500 = "home/500.html"
HTML_LOGIN = "home/login.html"
HTML_REGISTRATION_FORM = "registration/register.html"
HTML_SOCIAL_AUTH_FORM = "registration/social_auth_form.html"
HTML_STATS = "home/stats.html"

#E-mail Constants
EMAIL_SUBJECT_PETMATCH_PROPOSER='EmergencyPetMatcher: Your pet match is close to being successful!'
TEST_EMAIL="emergencypetmatchertest@gmail.com"
#Email Change.
TEXTFILE_EMAIL_CHANGE_BODY = "socializing/email_change_body.txt"
TEXTFILE_EMAIL_CHANGE_SUBJECT = "socializing/email_change_subject.txt"
#Post Guardian Activation Email
TEXTFILE_EMAIL_POST_GUARDIAN_ACTIVATION_SUBJECT = "registration/post_guardian_activation_subject.txt"
TEXTFILE_EMAIL_POST_GUARDIAN_ACTIVATION_BODY = "registration/post_guardian_activation_body.txt"
#Threshold reach Email.
TEXTFILE_EMAIL_PETMATCH_PROPOSER = "matching/verification_email_to_digital_volunteer.txt"
#Personal Messaging Email.
TEXTFILE_EMAIL_USERPROFILE_MESSAGE = "socializing/email_message_user.txt"
#Guardian for Minor Account Verification Email.
TEXTFILE_EMAIL_GUARDIAN_SUBJECT = "registration/guardian_email_subject.txt"
TEXTFILE_EMAIL_GUARDIAN_BODY = "registration/guardian_email.txt"


#General File Path Constants
PROJECT_WORKSPACE = os.path.dirname(__file__)
EPM_DIRECTORY = os.path.dirname(PROJECT_WORKSPACE)
LOGS_DIRECTORY = STATIC_URL + "logs/"

#Represents how many activities to fetch per request.
NUM_ACTIVITIES_HOMEPAGE = 20

#Activity Log File Path Constants
ACTIVITY_LOG_DIRECTORY = LOGS_DIRECTORY + "activity_logs/"

#Activities with their reward points attached.
ACTIVITIES = {  
  "ACTIVITY_ACCOUNT_CREATED"                : {"reward": 10,  "source":"userprofile"},
  "ACTIVITY_LOGIN"                          : {"reward":  0,  "source":"userprofile"},
  "ACTIVITY_LOGOUT"                         : {"reward":  0,  "source":"userprofile"},
  "ACTIVITY_USER_CHANGED_USERNAME"          : {"reward":  0,  "source":"userprofile"},
  "ACTIVITY_USER_SET_PHOTO"                 : {"reward":  2,  "source":"userprofile"},
  "ACTIVITY_SOCIAL_FOLLOW"                  : {"reward":  5,  "source":"userprofile"},
  "ACTIVITY_SOCIAL_UNFOLLOW"                : {"reward":  0,  "source":"userprofile"},
  "ACTIVITY_SOCIAL_SEND_MESSAGE_TO_USER"    : {"reward":  0,  "source":"userprofile"},                
  "ACTIVITY_PETREPORT_SUBMITTED"            : {"reward": 10,  "source":"petreport"},
  "ACTIVITY_PETREPORT_ADD_BOOKMARK"         : {"reward":  0,  "source":"petreport"},
  "ACTIVITY_PETREPORT_REMOVE_BOOKMARK"      : {"reward":  0,  "source":"petreport"},
  "ACTIVITY_PETMATCH_PROPOSED"              : {"reward": 15,  "source":"petmatch"},
  "ACTIVITY_PETMATCH_UPVOTE"                : {"reward":  2,  "source":"petmatch"},
  "ACTIVITY_PETMATCH_DOWNVOTE"              : {"reward":  2,  "source":"petmatch"},
  "ACTIVITY_PETMATCHCHECK_VERIFY"           : {"reward":  5,  "source":"petmatchcheck"},
  "ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS"   : {"reward": 20,  "source":"petmatchcheck"},
  "ACTIVITY_PETMATCHCHECK_VERIFY_FAIL"      : {"reward": 10,  "source":"petmatchcheck"},
  "ACTIVITY_PETREUNION_CREATED"             : {"reward": 10,  "source":"petreunion"}
}

ACTIVITY_SOCIAL_ACTIVITIES = [
  "ACTIVITY_ACCOUNT_CREATED",
  "ACTIVITY_USER_CHANGED_USERNAME",
  "ACTIVITY_USER_SET_PHOTO",
  "ACTIVITY_PETREPORT_SUBMITTED", 
  "ACTIVITY_PETMATCH_PROPOSED", 
  "ACTIVITY_PETMATCH_UPVOTE", 
  "ACTIVITY_PETMATCH_DOWNVOTE",
  "ACTIVITY_PETMATCHCHECK_VERIFY",
  "ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS",
  "ACTIVITY_PETMATCHCHECK_VERIFY_FAIL",
  "ACTIVITY_SOCIAL_FOLLOW",
  "ACTIVITY_PETREUNION_CREATED"
]

#Activity Model Field Length
ACTIVITIES_MAX_LENGTH = 50                              

CONSENT_FORM_MINOR_TEXT = """Welcome to EmergencyPetMatcher! 

We are researchers from Project EPIC (Empowering the Public with Information in Crisis) at the University of Colorado Boulder, and we are conducting a study to see how online volunteers help pet owners find their misplaced pets, as often happens when disaster strikes.

For this research, we will keep track of the information you provide to us, like the pets and pet matches you work on, which users you talk to, and how often you log on and use EPM. We will keep all of your information secure and private. Some information, such as your username, needs to be public so others on the web site know who you are. 

If you check the box below, it means that you have read this and that you want to work in EPM and be in this study. You will need to provide your parent/guardian's email address to make sure that they approve. You won't be able to register for EmergencyPetMatcher until we receive your parent's consent as well as yours.

If you don't want to be in the research, don't click the box, and that's okay because it's your choice.
 
You can ask questions now or later. You or your parents can contact us at emergencypetmatcher-support@googlegroups.com if you have a question. 

Thanks!
Project EPIC
"""

CONSENT_FORM_ADULT_TEXT = """Welcome to EmergencyPetMatcher! 

By checking the box below you indicate that you have read, understood, and agreed to the following:

EmergencyPetMatcher (EPM) is a tool developed and supported by the Project EPIC (Empowering the Public with Information in Crisis) research team at the University of Colorado Boulder. This research project is led by Leysia Palen (Professor of the Department of Computer Science, 430 UCB, palen@cs.colorado.edu).

Project Description: This project studies how people collect and share information about displaced pets in disaster events.  Your use of EPM will make you a participant in this research study.

Procedures: Researchers are interested in understanding your interaction with EPM and evaluating EPM's effectiveness in helping lost pets reunite with their families after a disaster. We will be able to see your interaction with the system in the form of data logs which we will examine after the fact and in collection with all the other users of the system. The data logs will indicate what pet reports users create, what pet matches users make, votes on matches, and following of and messaging to other users.  Private data including contact information (email address, date of birth), as well as personal messages between yourself and other users, will always be kept private and secure within our servers. They will not be exposed to others.

In addition, with your permission, researchers may contact you via email to inquire if you would be willing to participate in a questionnaire or interview about EPM. In all cases, when analyzing and reporting data gathered about your use of EPM, personal information will be removed.

Risks: There are no foreseeable risks in using EPM.  Please be aware the system is public to the outside world: the pet reports, pet matches, votes, and following activities you engage in are visible to everyone. Treat this content as you would treat content in other social networking sites you engage in, like Facebook or Twitter.

Benefits: There are no direct benefits to you by taking part in EmergencyPetMatcher, except that we hope that your work will reunite pets with their owners.

Privacy: You have the right to withdraw consent or stop participating at any time. If you do, you will no longer be able to use EPM. We will maintain the privacy of your data and not share it with anyone outside this research group. Your data will be kept secure. In any research reported we will use a pseudonym instead of your real name or EPM account name.  Choosing not to participate or withdrawing from participation involves no penalty or loss of other benefits to which a subject may be otherwise entitled.

Questions: If you have questions about this study, you may contact the EPM researchers at emergencypetmatcher-support@googlegroups.com before indicating your consent. If you have questions regarding your rights as a participant, any concerns about this project, or any dissatisfaction with any aspect of this study, you may report them - confidentially, if you wish - to the Institutional Review Board, 3100 Marine Street, Rm A15, 563 UCB, ph (303) 735-3702.

Following your agreement below, we take your ongoing use of the system to indicate your ongoing consent.

Thanks!
Project EPIC
"""

CONSENT_FORM_GUARDIAN_TEXT = """This consent form is to inform you that your child has registered for an account on the pet reporting and matching website, EmergencyPetMatcher (EPM) and to solicit your approval on your child's participation in EPM. We accept under-aged participation on EPM, but we do so only through child assent, or the consent of both the under-aged participant and his/her parent or guardian.

EmergencyPetMatcher (EPM) is a tool developed and supported by the Project EPIC (Empowering the Public with Information in Crisis) research team at the University of Colorado Boulder. This research project is led by Leysia Palen (Professor of the Department of Computer Science, 430 UCB, palen@cs.colorado.edu).

Project Description: This project studies how people collect and share information about displaced pets in disaster events. Your child's use of EPM will make him/her a participant in this research study.

Procedures: Researchers are interested in understanding your child's interaction with EPM and evaluating EPM's effectiveness in helping lost pets reunite with their families after a disaster. We will be able to see your child's interaction with the system in the form of data logs which we will examine after the fact and in aggregate with all the other users of the system. The data logs will indicate what pet reports users create, what pet matches users make, votes on matches, and following of and messaging to other users.  Private data including contact information (email address, date of birth), as well as personal messages between your child and other users, will always be kept private and secure within our servers. They will not be exposed to others.

In addition, with your permission, researchers may contact you and your child via email to inquire if he/she, with your permission would be willing to participate in a questionnaire or interview about EPM. In all cases, when analyzing and reporting data gathered about your child's use of EPM, personal information will be removed.

Risks: There are no foreseeable risks in using EPM. Please have your child be aware that the system is public to the outside world: the pet reports, pet matches, votes, and following activities your child engages in are visible to everyone. Treat this content as he/she would treat content in other social networking sites he/she engages in, like Facebook or Twitter.

Benefits: There are no direct benefits to you or your child in taking part in EmergencyPetMatcher, except that we hope that your child's work will reunite pets with their owners.

Privacy: Your child has the right to withdraw consent or stop participating at any time. If he/she does, he/she will no longer be able to use EPM. We will maintain the privacy of your child's data and not share it with anyone outside this research group. His/her data will be kept secure. In any research reported, we will use a pseudonym instead of your child's real name or EPM account name.  Choosing not to participate or withdrawing from participation involves no penalty or loss of other benefits to which a subject may be otherwise entitled.

Questions: If you have questions about this study, you or your child may contact the EPM researchers at emergencypetmatcher-support@googlegroups.com before indicating your consent. If you have questions regarding your child's rights as a participant, any concerns about this project, or any dissatisfaction with any aspect of this study, you may report them - confidentially, if you wish - to the Institutional Review Board, 3100 Marine Street, Rm A15, 563 UCB, ph (303) 735-3702.

Following your agreement below, we take your child's ongoing use of the system to indicate your ongoing consent.

Thanks!
Project EPIC

I have read this consent form. I know the possible risks and benefits of my child using EPM and I choose for him/her to be in this study. I know that being in this study is voluntary. I know that my child can withdraw at any time. 
"""



