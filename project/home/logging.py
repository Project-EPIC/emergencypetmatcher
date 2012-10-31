from constants import *
from home.models import UserProfile, PetReport, PetMatch
import os, sys, time
from django.utils import timezone 
from django.utils.dateparse import parse_datetime
from datetime import datetime

'''===================================================================================
[logging.py]: Logging Functionality for the EPM system
==================================================================================='''

'''Method for logging activities given an input UserProfile, Activity Enum, and (optionally) PetReport and PetMatch objects.'''
def log_activity(activity, userprofile, userprofile2=None, petreport=None, petmatch=None):
    assert isinstance(userprofile, UserProfile)

    #Define the user filename and logger.
    user = userprofile.user
    user_log_filename = ACTIVITY_LOG_DIRECTORY + user.username + ".log"
    # print user_log_filename
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

        elif activity == ACTIVITY_PETREPORT_ADD_BOOKMARK:
            assert isinstance(petreport, PetReport)
            log = "%s has added a PetReport bookmark for {%s} with ID{%d}\n" % (user.username, petreport.pet_name, petreport.id)

        elif activity == ACTIVITY_PETREPORT_REMOVE_BOOKMARK:
            assert isinstance(petreport, PetReport)
            log = "%s has removed a PetReport bookmark for {%s} with ID{%d}\n" % (user.username, petreport.pet_name, petreport.id)

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
 
        elif activity == ACTIVITY_FOLLOWING:
            assert isinstance(userprofile2, UserProfile)
            user2 = userprofile2.user
            log = "%s has followed {%s} with ID{%d}\n" % (user.username, user2.username, userprofile2.id)                 
 
            # Write the same following info into the follwer's log file
            user2_log_filename = ACTIVITY_LOG_DIRECTORY + user2.username + ".log"
            logger2 = open(user2_log_filename, "a")
            log2 = "%s has been followed by {%s} with ID{%d}\n" % (user2.username, user.username, userprofile.id)               
            log2 = (time.asctime() + " [%s]: " + log2) % ACTIVITY_FOLLOWER
            logger2.write(log2)
            logger2.close()

        elif activity == ACTIVITY_UNFOLLOWING:
            assert isinstance(userprofile2, UserProfile)
            user2 = userprofile2.user
            log = "%s has unfollowed {%s} with ID{%d}\n" % (user.username, user2.username, userprofile2.id)                 
 
            # Write the same unfollowing info into the unfollwer's log file
            user2_log_filename = ACTIVITY_LOG_DIRECTORY + user2.username + ".log"
            logger2 = open(user2_log_filename, "a")
            log2 = "%s has been unfollowed by {%s} with ID{%d}\n" % (user2.username, user.username, userprofile.id)               
            log2 = (time.asctime() + " [%s]: " + log2) % ACTIVITY_UNFOLLOWER
            logger2.write(log2)
            logger2.close()

        else:
            raise IOError

        if activity != ACTIVITY_LOGIN:
            log = (time.asctime() + " [%s]: " + log) % activity
            logger.write(log)
            logger.close()

    except IOError, AssertionError:
        print "[ERROR]: problem in log_activity()."
        

''' Helper function for returning an HTML representation for an input activity '''
def get_activity_HTML(log, userprofile, userprofile2=None, petreport=None, petmatch=None, current_userprofile=None):
    # print "in get_activity_HTML %s" % log
    
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

    elif ACTIVITY_PETREPORT_ADD_BOOKMARK in log:
        assert isinstance(petreport, PetReport)
        if petreport.pet_name.strip() == "unknown" or petreport.pet_name.strip() == "":
            html += "bookmarked a " + "<a class='prdp_dialog' href= '" + URL_PRDP + str(petreport.id) + "/'>" + "Pet Report </a> with no name."
        else:
            html += "bookmarked a Pet Report named <a class='prdp_dialog' href= '" + URL_PRDP + str(petreport.id) + "/'>" + petreport.pet_name + "</a>!"

    elif ACTIVITY_PETMATCH_PROPOSED in log:
        assert isinstance(petmatch, PetMatch)
        html += "proposed a <a class='pmdp_dialog' href='" + URL_PMDP + str(petmatch.id) + "/'>" + "Pet Match</a> examining two " + petmatch.lost_pet.pet_type + "s!"

    elif ACTIVITY_PETMATCH_PROPOSED_LOST_BOOKMARKED_PETREPORT in log:
        assert isinstance(petmatch, PetMatch)  
        assert isinstance(userprofile, UserProfile)
        html = "Bookmark: <a href='" + URL_USERPROFILE + str(userprofile.id) + "/'>" + userprofile.user.username + "</a> "
        html += "proposed a <a class='pmdp_dialog' href='" + URL_PMDP + str(petmatch.id) + "/'>" + "Pet Match</a>"
        html += " for " + petmatch.lost_pet.status + " <a class='prdp_dialog' href= '" + URL_PRDP + str(petmatch.lost_pet.id) + "/'>" + petmatch.lost_pet.pet_name + "</a>." 

    elif ACTIVITY_PETMATCH_PROPOSED_FOUND_BOOKMARKED_PETREPORT in log:
        assert isinstance(petmatch, PetMatch) 
        assert isinstance(userprofile, UserProfile) 
        html = "Bookmark: <a href='" + URL_USERPROFILE + str(userprofile.id) + "/'>" + userprofile.user.username + "</a> "
        html += "proposed a <a class='pmdp_dialog' href='" + URL_PMDP + str(petmatch.id) + "/'>" + "Pet Match</a> "
        html += "for " + petmatch.found_pet.status + " <a class='prdp_dialog' href= '" + URL_PRDP + str(petmatch.found_pet.id) + "/'>" + petmatch.found_pet.pet_name + "</a>." 

    elif ACTIVITY_PETMATCH_UPVOTE in log:
        assert isinstance(petmatch, PetMatch)
        html += "upvoted a <a class='pmdp_dialog' href='" + URL_PMDP + str(petmatch.id) + "/'>" + "Pet Match</a> examining two " + petmatch.lost_pet.pet_type + "s!"

    elif ACTIVITY_PETMATCH_DOWNVOTE in log:
        assert isinstance(petmatch, PetMatch)
        html += "downvoted a <a class='pmdp_dialog' href='" + URL_PMDP + str(petmatch.id) + "/'>" + "Pet Match</a> examining two " + petmatch.lost_pet.pet_type + "s!"

    elif ACTIVITY_FOLLOWING in log:
        assert isinstance(userprofile, UserProfile)
        assert isinstance(userprofile2, UserProfile)
        if userprofile2 == current_userprofile:
            html = ""
        else:
            html += "has followed <a href='" + URL_USERPROFILE + str(userprofile2.id) + "/'>" + userprofile2.user.username + "</a> "

    elif ACTIVITY_FOLLOWER in log:
        assert isinstance(userprofile, UserProfile)
        assert isinstance(userprofile2, UserProfile)
        # If a user has followed the same current UserProfile, use the pronoun 'you'
        if userprofile == current_userprofile:
            html = "<a href='" + URL_USERPROFILE + str(userprofile2.id) + "/'>" + userprofile2.user.username + "</a> has followed you!"
        # If a user has been followed by the same current UserProfile, no need to show this information
        elif userprofile2 == current_userprofile:
            html = ""
        else:
            html += "has been followed by <a href='" + URL_USERPROFILE + str(userprofile2.id) + "/'>" + userprofile2.user.username + "</a> "

    return html



'''Helper function to get the most recent activity from an input UserProfile and (optionally) activity type.'''
def get_recent_activites_from_log(userprofile, current_userprofile=None, since_date=None, num_activities=100, activity=None):

    assert isinstance(userprofile, UserProfile)
    if current_userprofile !=None:
        assert isinstance(current_userprofile, UserProfile)

    # Define the user filename and logger.
    user = userprofile.user
    user_log_filename = ACTIVITY_LOG_DIRECTORY + user.username + ".log"
    print user_log_filename
    recent_log = None

    # Initialize the activity list
    activities = [] 

    with open(user_log_filename, 'r') as logger:

        reversed_activities = iter(reversed(logger.readlines()))
        petreport = None
        petmatch = None
        userprofile2 = None
        num_log = 0
 
        if since_date == None:
            since_date = datetime.strptime("1/1/1900", '%m/%d/%Y')
        else: 
            since_date = datetime.strptime(str(since_date)[:19], '%Y-%m-%d %H:%M:%S')     
        # Reference: http://docs.python.org/library/time.html#time.strptime
        # http://agiliq.com/blog/2009/02/understanding-datetime-tzinfo-timedelta-amp-timezo/
 
        # Iterate through the log file.
        for line in reversed_activities:

            # Before we do any work, check if the activity does not exist in this line.
            if (activity != None) and (activity not in line):
                continue  

            # Get the log date from each line in the log file
            log_date = datetime.strptime(line[:24], '%a %b %d %H:%M:%S %Y')
  
            # If the log date is older than since_date, or 
            # If the number of retrieved log is greater than num_activities 
            # Break the loop and close the log file
            if (log_date < since_date) or (num_log >= num_activities):
                break
  
            # Every line has an ID to denote what is being identified (PetMatchc, UserProfile, etc).
            identifier = line.split("ID")[1].replace('}','').replace('{','')   

            if ACTIVITY_ACCOUNT_CREATED in line:
                recent_log = line
                # print "recent_log: %s" % recent_log
            elif ACTIVITY_PETREPORT_SUBMITTED in line:
                petreport = PetReport.objects.get(pk=int(identifier))
                recent_log = line     
                # print "recent_log: %s" % recent_log
            elif ACTIVITY_PETREPORT_ADD_BOOKMARK in line:
                petreport = PetReport.objects.get(pk=int(identifier))
                recent_log = line                    
                # print "recent_log: %s" % recent_log
            elif ACTIVITY_PETMATCH_PROPOSED in line:
                petmatch = PetMatch.objects.get(pk=int(identifier))
                recent_log = line                    
                # print "recent_log: %s" % recent_log
            elif ACTIVITY_PETMATCH_UPVOTE in line:
                petmatch = PetMatch.objects.get(pk=int(identifier))
                recent_log = line                    
                # print "recent_log: %s" % recent_log
            elif ACTIVITY_PETMATCH_DOWNVOTE in line:
                petmatch = PetMatch.objects.get(pk=int(identifier))
                recent_log = line  
                # print "recent_log: %s" % recent_log
            elif ACTIVITY_FOLLOWING in line:
                userprofile2 = UserProfile.objects.get(pk=int(identifier))
                recent_log = line 
                # print "recent_log: %s" % recent_log
            elif ACTIVITY_FOLLOWER in line:
                userprofile2 = UserProfile.objects.get(pk=int(identifier))
                recent_log = line 
                # print "recent_log: %s" % recent_log
            else:
                continue

            num_log = num_log + 1

            if recent_log != None:   
                feed = get_activity_HTML(recent_log, userprofile, userprofile2=userprofile2, petreport=petreport, petmatch=petmatch, current_userprofile=current_userprofile)
                if feed not in activities and feed!="":
                    activities.append([str(log_date),feed])

    logger.close()
    return activities


def get_bookmark_activities(userprofile, since_date=None):
    assert isinstance(userprofile, UserProfile)

    if since_date == None:
        since_date = datetime.strptime("1/1/1900", '%m/%d/%Y')
    else: 
        since_date = datetime.strptime(str(since_date)[:19], '%Y-%m-%d %H:%M:%S')

    # Initialize the activity list
    activities = [] 

    # Loop through all bookmarked PetReports for this UserProfile
    for bookmarked_petreport in userprofile.bookmarks_related.all():

        if bookmarked_petreport.status == "Lost":
            related_petmatches = bookmarked_petreport.lost_pet_related.all()
            activity = ACTIVITY_PETMATCH_PROPOSED_LOST_BOOKMARKED_PETREPORT

        elif bookmarked_petreport.status == "Found":
            related_petmatches = bookmarked_petreport.found_pet_related.all()
            activity = ACTIVITY_PETMATCH_PROPOSED_FOUND_BOOKMARKED_PETREPORT

        for related_petmatch in related_petmatches:

            # If the log date is older than the last logout date, or
            # If the pet match proposer is the same as the current UserProfile, 
            # Ignore that activity            
            proposed_date = datetime.strptime(str(related_petmatch.proposed_date)[:19], '%Y-%m-%d %H:%M:%S')
            if proposed_date < since_date or related_petmatch.proposed_by == userprofile:
                continue

            # Create a temp log
            log = "%s proposed the PetMatch object with ID{%d}\n" % (related_petmatch.proposed_by.user.username, related_petmatch.id)
            log = (" [%s]: " + log) % activity
            activities.append([str(proposed_date),get_activity_HTML(log, related_petmatch.proposed_by, userprofile2=None, petreport=None, petmatch=related_petmatch)])

    return activities



'''Helper function to determine if the input activity has been logged in the past'''
def activity_has_been_logged(activity, userprofile, userprofile2=None, petreport=None, petmatch=None):
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

    print "The file %s was not found in the activity log directory" % user_log_filename
    return False
            




