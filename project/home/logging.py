from constants import *
from home.models import UserProfile, PetReport, PetMatch
import os, sys, time

'''===================================================================================
[logging.py]: Logging Functionality for the EPM system
==================================================================================='''

'''Method for logging activities given an input UserProfile, Activity Enum, and (optionally) PetReport and PetMatch objects.'''
def log_activity (activity, userprofile, petreport=None, petmatch=None):
    assert isinstance(userprofile, UserProfile)

    #Define the user filename and logger.
    user = userprofile.user
    user_log_filename = ACTIVITY_LOG_DIRECTORY + user.username + ".log"

    try:
        logger = open(user_log_filename, "a")
        if activity == ACTIVITY_ACCOUNT_CREATED:
            log = "A new UserProfile account was created for {%s} with ID{%d}\n" % (user.username, userprofile.id)

        elif activity == ACTIVITY_LOGIN:
            log = "%s with ID{%d} logged in to the system\n" % (user.username, userprofile.id)            

        elif activity == ACTIVITY_LOGOUT:
            log = "%s with ID{%d} logged out of the system\n" % (user.username, userprofile.id)            

        elif activity == ACTIVITY_PETREPORT_SUBMITTED:
            assert isinstance(petreport, PetReport)
            log = "%s submitted the PetReport for {%s} with ID{%d}\n" % (user.username, petreport.pet_name, petreport.id)

        elif activity == ACTIVITY_PETMATCH_PROPOSED:
            assert isinstance(petmatch, PetMatch)
            log = "%s proposed the PetMatch object with ID{%d}\n" % (user.username, petmatch.id)

        elif activity == ACTIVITY_PETMATCH_UPVOTE:
            print petmatch
            assert isinstance(petmatch, PetMatch)
            log = "%s upvoted the PetMatch object with ID{%d}\n" % (user.username, petmatch.id)

        elif activity == ACTIVITY_PETMATCH_DOWNVOTE:
            assert isinstance(petmatch, PetMatch)
            log = "%s downvoted the PetMatch object with ID{%d}\n" % (user.username, petmatch.id)         

        else:
            raise IOError

        log = (time.asctime() + " [%s]: " + log) % activity
        print log
        logger.write(log)
        logger.close()

    except IOError, AssertionError:
        print "[ERROR]: problem in log_activity()."
        

''' Helper function for returning an HTML representation for an input activity '''
def get_activity_HTML(log, userprofile, petreport=None, petmatch=None):
    print "in get_activity_HTML %s" % log
    log = log.strip()
    html = "<a href='" + URL_USERPROFILE + str(userprofile.id) + "/'>" + userprofile.user.username + "</a> "

    if ACTIVITY_ACCOUNT_CREATED in log:
        assert isinstance(userprofile, UserProfile)
        html += "has just joined EPM!"

    elif ACTIVITY_PETREPORT_SUBMITTED in log:
        assert isinstance(petreport, PetReport)
        if petreport.pet_name.strip() == "unknown" or petreport.pet_name.strip() == "":
            html += "submitted a " + "<a class='prdp_dialog' href= '" + URL_PRDP + str(petreport.id) + "/'>" + "Pet Report </a> with no name."
        else:
            html += "submitted a Pet Report named <a class='prdp_dialog' href= '" + URL_PRDP + str(petreport.id) + "/'>" + petreport.pet_name + "</a>!"

    elif ACTIVITY_PETMATCH_PROPOSED in log:
        assert isinstance(petmatch, PetMatch)
        html += "proposed a <a class='prdp_dialog' href='" + URL_PMDP + str(petmatch.id) + "/'>" + "Pet Match </a> examining two " + petmatch.lost_pet.pet_type + "s!"

    elif ACTIVITY_PETMATCH_UPVOTE in log:
        assert isinstance(petmatch, PetMatch)
        html += "upvoted a <a class='pmdp_dialog' href='" + URL_PMDP + str(petmatch.id) + "/'>" + "Pet Match </a> examining two " + petmatch.lost_pet.pet_type + "s!"

    elif ACTIVITY_PETMATCH_DOWNVOTE in log:
        assert isinstance(petmatch, PetMatch)
        html += "downvoted a <a class='pmdp_dialog' href='" + URL_PMDP + str(petmatch.id) + "/'>" + "Pet Match </a> examining two " + petmatch.lost_pet.pet_type + "s!"

    return html


'''Helper function to get the most recent activity from an input UserProfile and (optionally) activity type.'''
def get_recent_log(userprofile, activity=None):
    assert isinstance(userprofile, UserProfile)
    #Define the user filename and logger.
    user = userprofile.user
    user_log_filename = ACTIVITY_LOG_DIRECTORY + user.username + ".log"
    print user_log_filename
    recent_log = None

    with open(user_log_filename, 'r') as logger:

        #WARNING: Linear-time operation - does NOT scale well.
        #Create a list iterator that can traverse over the lines of
        #the log in reverse order.
        reversed_activities = iter(reversed(logger.readlines()))
        petreport = None
        petmatch = None

        #Iterate only once UNLESS an activity has been specified and found.
        for line in reversed_activities:

            #Before we do any work, check if the activity does not exist in this line.
            if (activity != None) and (activity not in line):
                continue

            #Every line has an ID to denote what is being identified (PetMatchc, UserProfile, etc).
            identifier = line.split("ID")[1].replace('}','').replace('{','')   

            if ACTIVITY_ACCOUNT_CREATED in line: 
                recent_log = line
            elif ACTIVITY_PETREPORT_SUBMITTED in line:
                petreport = PetReport.objects.get(pk=int(identifier))
                recent_log = line                    
            elif ACTIVITY_PETMATCH_PROPOSED in line:
                petmatch = PetMatch.objects.get(pk=int(identifier))
                recent_log = line                    
            elif ACTIVITY_PETMATCH_UPVOTE in line:
                petmatch = PetMatch.objects.get(pk=int(identifier))
                recent_log = line                    
            elif ACTIVITY_PETMATCH_DOWNVOTE in line:
                petmatch = PetMatch.objects.get(pk=int(identifier))
                recent_log = line  
            else:
                continue

            if activity != None:
                if activity in recent_log:
                    break
                else:
                    continue
            else:
                break

    
    if recent_log == None:
        return "" #No log to return.
    else:    
        return get_activity_HTML(recent_log, userprofile, petreport=petreport, petmatch=petmatch)


'''Helper function to determine if the input activity has been logged in the past'''
def activity_has_been_logged (activity, userprofile, petreport=None, petmatch=None):
    assert isinstance(userprofile, UserProfile)

    #Define the user filename and logger.
    user = userprofile.user
    user_log_filename = ACTIVITY_LOG_DIRECTORY + user.username + ".log"

    #If this particular user log file exists, then continue.
    if os.path.exists(user_log_filename) == True:
        logger = open(user_log_filename, "r")

        #iterate through all lines in the log file and find an activity match.
        for line in iter(lambda:logger.readline(), ""):
            if (activity in line) and (user.username in line):
                identifier = line.split("ID")[1]

                if activity == ACTIVITY_ACCOUNT_CREATED:
                    if str(userprofile.id) in identifier:
                        logger.close()
                        return True

                if activity == ACTIVITY_LOGIN:
                    if str(userprofile.id) in identifier:
                        logger.close()
                        return True                        

                if activity == ACTIVITY_LOGOUT:
                    if str(userprofile.id) in identifier:
                        logger.close()
                        return True                                                

                elif activity == ACTIVITY_PETREPORT_SUBMITTED:
                    assert isinstance(petreport, PetReport)
                    if str(petreport.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_PETMATCH_PROPOSED:
                    assert isinstance(petmatch, PetMatch)
                    if str(petmatch.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_PETMATCH_UPVOTE:
                    assert isinstance(petmatch, PetMatch)
                    if str(petmatch.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_PETMATCH_DOWNVOTE:
                    assert isinstance(petmatch, PetMatch)
                    if str(petmatch.id) in identifier:
                        logger.close()
                        return True

        logger.close()
        return False

    print "The file %s was not found in the activity log directory" % user_log_filename
    return False
            




