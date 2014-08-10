from utilities.utils import print_debug_msg
from django.utils import timezone 
from django.utils.dateparse import parse_datetime
from datetime import datetime
from pprint import pprint
from verifying.models import PetCheck
from matching.models import PetMatch
from reporting.models import PetReport
from social.models import UserProfile
from home.constants import *
import os, sys, time, re, documenter

'''===================================================================================
[logger.py]: Logging Functionality for the EPM system
==================================================================================='''

'''Method for logging activities given an input UserProfile, Activity Enum, and (optionally) PetReport and PetMatch objects.'''
def log_activity(activity, userprofile, userprofile2=None, petreport=None, petmatch=None):
    assert isinstance(userprofile, UserProfile)
    user = userprofile.user
    log = {}
    activity_type = None 

    try:
        # ============================= [Main and UserProfile Activities] =============================

        if activity == ACTIVITY_ACCOUNT_CREATED:
            log[DOCUMENTER_KEY_LOG] = "A new UserProfile account was created for {%s} with ID{%d}" % (user.username, userprofile.id)
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE

        elif activity == ACTIVITY_LOGIN:
            log[DOCUMENTER_KEY_LOG] = "%s with ID{%d} logged in to the system" % (user.username, userprofile.id)           
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE

        elif activity == ACTIVITY_LOGOUT:
            log[DOCUMENTER_KEY_LOG] = "%s with ID{%d} logged out of the system" % (user.username, userprofile.id)            
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE

        elif activity == ACTIVITY_USER_CHANGED_USERNAME:
            log[DOCUMENTER_KEY_LOG] = "%s with ID{%d} renamed his/her username" % (user.username, userprofile.id)
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE

        elif activity == ACTIVITY_FOLLOWING:
            assert isinstance(userprofile2, UserProfile)
            log[DOCUMENTER_KEY_LOG] = "%s has followed {%s} with ID{%d}" % (user.username, userprofile2.user.username, userprofile2.id)                 
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE

            # Write the same following info into the follower's log file
            log_activity(ACTIVITY_FOLLOWER, userprofile=userprofile2, userprofile2=userprofile)

        elif activity == ACTIVITY_UNFOLLOWING:
            assert isinstance(userprofile2, UserProfile)
            log[DOCUMENTER_KEY_LOG] = "%s has unfollowed {%s} with ID{%d}" % (user.username, userprofile2.user.username, userprofile2.id)                 
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE

            # Write the same unfollowing info into the unfollower's log file
            log_activity(ACTIVITY_UNFOLLOWER, userprofile=userprofile2, userprofile2=userprofile)
  
        elif activity == ACTIVITY_FOLLOWER:
            assert isinstance(userprofile2, UserProfile)
            log[DOCUMENTER_KEY_LOG] = "%s has been followed by {%s} with ID{%d}" % (user.username, userprofile2.user.username, userprofile2.id)                           
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE

        elif activity == ACTIVITY_UNFOLLOWER:
            assert isinstance(userprofile2, UserProfile)
            log[DOCUMENTER_KEY_LOG] = "%s has been unfollowed by {%s} with ID{%d}" % (user.username, userprofile2.user.username, userprofile2.id)                           
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE


        # ============================= [PetReport Activities] =============================

        elif activity == ACTIVITY_PETREPORT_SUBMITTED:
            assert isinstance(petreport, PetReport)
            log[DOCUMENTER_KEY_LOG] = "%s submitted the PetReport for {%s} with ID{%d}" % (user.username, petreport.pet_name, petreport.id)
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_PETREPORT

        elif activity == ACTIVITY_PETREPORT_ADD_BOOKMARK:
            assert isinstance(petreport, PetReport)
            log[DOCUMENTER_KEY_LOG] = "%s has added a PetReport bookmark for {%s} with ID{%d}" % (user.username, petreport.pet_name, petreport.id)
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_PETREPORT

        elif activity == ACTIVITY_PETREPORT_REMOVE_BOOKMARK:
            assert isinstance(petreport, PetReport)
            log[DOCUMENTER_KEY_LOG] = "%s has removed a PetReport bookmark for {%s} with ID{%d}" % (user.username, petreport.pet_name, petreport.id)
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_PETREPORT


        # ============================= [PetMatch Activities] =============================

        elif activity == ACTIVITY_PETMATCH_PROPOSED:
            assert isinstance(petmatch, PetMatch)
            log[DOCUMENTER_KEY_LOG] = "%s proposed the PetMatch object with ID{%d}" % (user.username, petmatch.id)
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_PETMATCH

        elif activity == ACTIVITY_PETMATCH_UPVOTE:
            assert isinstance(petmatch, PetMatch)
            log[DOCUMENTER_KEY_LOG] = "%s upvoted the PetMatch object with ID{%d}" % (user.username, petmatch.id)
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_PETMATCH

        elif activity == ACTIVITY_PETMATCH_DOWNVOTE:
            assert isinstance(petmatch, PetMatch)
            log[DOCUMENTER_KEY_LOG] = "%s downvoted the PetMatch object with ID{%d}" % (user.username, petmatch.id)  
            activity_type = DOCUMENTER_ACTIVITY_COLLECTION_PETMATCH
 
        else:
            raise IOError
      
        log[DOCUMENTER_KEY_DATE] = time.asctime()
        log[DOCUMENTER_KEY_ACTIVITY] = activity

        #Decide which collection to log the activity.
        if activity_type == DOCUMENTER_ACTIVITY_COLLECTION_USERPROFILE:
            documenter.insert_into_UserProfiles(log)
        elif activity_type == DOCUMENTER_ACTIVITY_COLLECTION_PETREPORT:
            documenter.insert_into_PetReports(log)
        elif activity_type == DOCUMENTER_ACTIVITY_COLLECTION_PETMATCH:            
            documenter.insert_into_PetMatches(log)

    except Exception as e:
        print "[ERROR]: problem in logger.log_activity(%s)." % e
        

''' Helper function for returning a dictionary for an input activity '''
def get_activity_payload(logline, userprofile, current_userprofile, userprofile2=None, petreport=None, petmatch=None):
    assert isinstance(userprofile, UserProfile)
    logline = logline.strip()

    # Every line has an ID to denote what is being identified (PetMatch, UserProfile, etc).
    identifier = re.search("\{(\d*)\}", logline)
    identifier = int(identifier.group(1))    

    #Grab the activity enum.
    log_activity = re.search("\[(.*)\]", logline)
    log_activity = log_activity.group(1)

    #Debug messages (remove when ready to deploy).
    #print "get_activity_payload() =========="
    #print "ID FOUND: {%d}" % identifier
    #print "ACTIVITY FOUND: {%s}" % log_activity    

    #Form the activity payload.
    activity = {"userprofile_username":userprofile.user.username, "userprofile_id":str(userprofile.id)}

    try:
        #If we have a current_userprofile (i.e. authenticated user)
        if current_userprofile != None:
            activity ["current_userprofile_id"] = str(current_userprofile.id)

        #Begin the *switch* structure for activity payload forming.
        if log_activity == ACTIVITY_ACCOUNT_CREATED:
            activity ["activity"] = ACTIVITY_ACCOUNT_CREATED

        elif log_activity == ACTIVITY_PETREPORT_SUBMITTED:
            if petreport == None:
                petreport = PetReport.objects.get(pk=identifier)

            assert isinstance(petreport, PetReport)
            activity ["activity"] = ACTIVITY_PETREPORT_SUBMITTED
            activity ["petreport_id"] = str(petreport.id)
            
            if petreport.pet_name.strip() == "unknown" or petreport.pet_name.strip() == "":
                activity ["petreport_name"] = None
            else:
                activity ["petreport_name"] = petreport.pet_name

        elif log_activity == ACTIVITY_PETREPORT_ADD_BOOKMARK:
            if petreport == None:
                petreport = PetReport.objects.get(pk=identifier)

            assert isinstance(petreport, PetReport)
            activity ["activity"] = ACTIVITY_PETREPORT_ADD_BOOKMARK
            activity ["petreport_id"] = str(petreport.id)        
            activity ["petreport_name"] = petreport.pet_name

        elif log_activity == ACTIVITY_PETMATCH_PROPOSED:
            if petmatch == None:
                petmatch = PetMatch.objects.get(pk=identifier)

            assert isinstance(petmatch, PetMatch)
            activity ["activity"] = ACTIVITY_PETMATCH_PROPOSED
            activity ["petmatch_id"] = str(petmatch.id)
            activity ["petmatch_type"] = petmatch.lost_pet.pet_type
            activity ["lostpet_name"] = petmatch.lost_pet.pet_name
            activity ["foundpet_name"] = petmatch.found_pet.pet_name

        elif log_activity == ACTIVITY_PETMATCH_PROPOSED_FOR_BOOKMARKED_PETREPORT:
            if petreport == None:
                petreport = PetReport.objects.get(pk=identifier)
            if petmatch == None:
                petmatch = PetMatch.objects.get(pk=identifier)

            assert isinstance(petmatch, PetMatch)
            assert isinstance(petreport, PetReport)
            activity ["activity"] = ACTIVITY_PETMATCH_PROPOSED_FOR_BOOKMARKED_PETREPORT
            activity ["petmatch_id"] = str(petmatch.id)
            activity ["lostpet_name"] = petmatch.lost_pet.pet_name
            activity ["foundpet_name"] = petmatch.found_pet.pet_name        
            activity ["petreport_id"] = str(petreport.id)
            activity ["petreport_name"] = petreport.pet_name

        elif log_activity == ACTIVITY_PETMATCH_UPVOTE or log_activity == ACTIVITY_PETMATCH_DOWNVOTE:
            if petmatch == None:
                petmatch = PetMatch.objects.get(pk=identifier)

            assert isinstance(petmatch, PetMatch)
            activity ["activity"] = "ACTIVITY_PETMATCH_VOTE"
            activity ["petmatch_id"] = str(petmatch.id)
            activity ["petmatch_type"] = petmatch.lost_pet.pet_type
            activity ["lostpet_name"] = petmatch.lost_pet.pet_name
            activity ["foundpet_name"] = petmatch.found_pet.pet_name        

        elif log_activity == ACTIVITY_FOLLOWING:
            if userprofile2 == None:
                userprofile2 = UserProfile.objects.get(pk=identifier)

            assert isinstance(userprofile2, UserProfile)
            activity ["activity"] = ACTIVITY_FOLLOWING
            activity ["userprofile2_id"] = str(userprofile2.id)
            activity ["userprofile2_username"] = userprofile2.user.username

        elif log_activity == ACTIVITY_FOLLOWER:
            if userprofile2 == None:
                userprofile2 = UserProfile.objects.get(pk=identifier)

            assert isinstance(userprofile2, UserProfile)
            activity ["activity"] = ACTIVITY_FOLLOWER
            activity ["userprofile2_id"] = str(userprofile2.id)
            activity ["userprofile2_username"] = userprofile2.user.username

        else:
            return None #We don't want to return payloads for some activities (e.g. ACTIVITY_LOGIN).
        
    #Sometimes, we don't get so lucky and the Model object isn't found in the DB. Warn and then return None.
    except Exception as e:
        print ("ERROR in Logger.get_activity_payload():[%s]" % e)
        return None 

    return activity


    # Helper function to get the most recent activity from an input UserProfile and (optionally) activity type. 
    # [userprofile]: the userprofile whose log file is read to get recent activity feeds
    # [since_date]: used to get all log activities that happened since that date 
    # [num_activities]: used to get a number of activities not more than this number
    # [activity]: used to decide about one type of activity and ignore the other
def get_activities_from_log(userprofile, since_date=None, num_activities=10, activity=None):
    assert isinstance(userprofile, UserProfile)
    activities = [] 

    # Reference: http://docs.python.org/library/time.html#time.strptime
    # http://agiliq.com/blog/2009/02/understanding-datetime-tzinfo-timedelta-amp-timezo/     
    if since_date == None:
        since_date = datetime.strptime("1/1/1900", '%m/%d/%Y')
    else:
        since_date = datetime.strptime(str(since_date)[:19], '%Y-%m-%d %H:%M:%S')

    #Query the documenter and receive all activities valid for this request.
    activities = documenter.get_activities_for_feed(userprofile.id, since_date, limit=num_activities)
    return activities


def get_bookmarking_activities_from_log(userprofile, since_date=None, num_activities=10):
    assert isinstance(userprofile, UserProfile)

    if since_date == None:
        since_date = datetime.strptime("1/1/1900", '%m/%d/%Y')
    else: 
        since_date = datetime.strptime(str(since_date)[:19], '%Y-%m-%d %H:%M:%S')

    # Initialize the activity list
    activities = [] 
    num_log = 0

    # Loop through all bookmarked PetReports for this UserProfile
    for bookmarked_petreport in userprofile.bookmarks_related.all():

        if bookmarked_petreport.status == "Lost":
            related_petmatches = bookmarked_petreport.lost_pet_related.all()

        elif bookmarked_petreport.status == "Found":
            related_petmatches = bookmarked_petreport.found_pet_related.all()

        for related_petmatch in related_petmatches:

            #If we've passed our number of activities limit, stop.
            if num_log > num_activities:
                break            

            # If the log date is older than the last logout date, or
            # If the pet match proposer is the same as the current UserProfile, 
            # Ignore that activity            
            proposed_date = datetime.strptime(str(related_petmatch.proposed_date)[:19], '%Y-%m-%d %H:%M:%S')
            if proposed_date < since_date or related_petmatch.proposed_by == userprofile:
                continue

            #pprint ("[DEBUG]: bookmarked_petreport: %s" % bookmarked_petreport)
            #pprint ("[DEBUG]: related_petmatch: %s" % related_petmatch)

            # Create a temp log
            log = "%s proposed the PetMatch object with ID{%d} for bookmarked PetReport object with ID{%d} \n" % (related_petmatch.proposed_by.user.username, related_petmatch.id, bookmarked_petreport.id)
            log = ("[%s]: " + log) % ACTIVITY_PETMATCH_PROPOSED_FOR_BOOKMARKED_PETREPORT
            activity_payload = get_activity_payload(log, userprofile=related_petmatch.proposed_by, current_userprofile=related_petmatch.proposed_by, userprofile2=None, petreport=bookmarked_petreport, petmatch=related_petmatch)

            #If the activity is good, then +1.
            if activity_payload != None:
                num_log += 1
                activities.append([str(proposed_date), activity_payload])

    return activities


'''Helper function to determine if the input activity has been logged in the past'''
def activity_has_been_logged(activity, userprofile, userprofile2=None, petreport=None, petmatch=None):
    assert isinstance(userprofile, UserProfile)

    #Define the user filename and logger.
    user = userprofile.user
    user_log_filename = ACTIVITY_LOG_DIRECTORY + str(userprofile.id) + ".log"

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

                elif activity == ACTIVITY_LOGIN:
                    if str(userprofile.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_LOGOUT:
                    if str(userprofile.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_USER_CHANGED_USERNAME:
                    if str(userprofile.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_PETREPORT_SUBMITTED:
                    assert isinstance(petreport, PetReport)
                    if str(petreport.id) in identifier:
                        logger.close()
                        return True
 
                elif activity == ACTIVITY_PETREPORT_ADD_BOOKMARK:
                    assert isinstance(petreport, PetReport)
                    if str(petreport.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_PETREPORT_REMOVE_BOOKMARK:
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

                elif activity == ACTIVITY_FOLLOWING:
                    assert isinstance(userprofile2, UserProfile)
                    if str(userprofile2.user.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_FOLLOWER:
                    assert isinstance(userprofile2, UserProfile)
                    if str(userprofile2.user.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_UNFOLLOWING:
                    assert isinstance(userprofile2, UserProfile)
                    if str(userprofile2.user.id) in identifier:
                        logger.close()
                        return True

                elif activity == ACTIVITY_UNFOLLOWER:
                    assert isinstance(userprofile2, UserProfile)
                    if str(userprofile2.user.id) in identifier:
                        logger.close()
                        return True

        logger.close()
        return False

    print "[ERROR]: The file (%s) was not found in the activity log directory." % user_log_filename
    return False


#Given a UserProfile instance, return True if its log file exists, False otherwise.
def log_exists (userprofile):
    assert isinstance(userprofile, UserProfile)
    log_path = ACTIVITY_LOG_DIRECTORY + str(userprofile.id) + ".log" 

    if os.path.isfile(log_path):
        return True
    else:
        return False


#Given a UserProfile instance, delete its log file.
def delete_log (userprofile):
    assert isinstance(userprofile, UserProfile)
    log_path = ACTIVITY_LOG_DIRECTORY + str(userprofile.id) + ".log" 

    if os.path.isfile(log_path):
        try:
            os.unlink(log_path)
            print "[OK]: UserProfile log file was deleted in (%s)" % log_path

        except Exception as e:
            print "[ERROR]: Could not delete UserProfile log file (%s)" % e
    else:
        print "[ERROR]: Could not find UserProfile log file in (%s).\nDid you set one up for this UserProfile?" % log_path
          

