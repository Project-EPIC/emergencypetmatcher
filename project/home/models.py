from django.db import models
from utilities.utils import *
from constants import *

#The Activity Object Model
class Activity(models.Model):
  userprofile = models.ForeignKey("socializing.UserProfile", null=False, default=None)
  source_id = models.IntegerField(null=False, default=None)
  activity = models.CharField(max_length=ACTIVITIES_MAX_LENGTH, choices=(zip(ACTIVITIES.keys(), ACTIVITIES.keys())), null=False, default=None)
  date_posted = models.DateField(null=False, auto_now_add=True)
  text = models.CharField(max_length=150, null=False, default=None)

  @staticmethod
  def get_activities_for_feed(since_date, page, userprofile=None, limit=10):
    total_activities = []

    for activity in ACTIVITY_SOCIAL_ACTIVITIES:
      if userprofile != None:
        total_activities += Activity.objects.filter(userprofile=userprofile, activity=activity, date_posted=since_date)[:5]
      else:
        total_activities += Activity.objects.filter(activity=activity, date_posted=since_date)[:5]
        
    #Total # activities must be less than or equal to specified limit.
    print total_activities
    total_activities = sorted(total_activities, key=lambda activity: activity.date_posted)[:limit]
    return total_activities  

    @staticmethod
    def get_PetReports_by_page(filtered_petreports, page):
        if (page != None and page > 0):
            page = int(page)
            filtered_petreports = filtered_petreports [((page-1) * NUM_PETREPORTS_HOMEPAGE):((page-1) * NUM_PETREPORTS_HOMEPAGE + NUM_PETREPORTS_HOMEPAGE)]

        #Just return the list of PetReports.
        return filtered_petreports 

  #Method for logging activities given an Activity constant, input UserProfile, and a source object.
  @staticmethod
  def log_activity(activity, userprofile, source=None):
    if activity not in ACTIVITIES.keys():
      print_error_msg("Activity Type %s does not exist." % activity)
      return None

    #Create a new Activity object.
    new_activity = Activity()
    new_activity.userprofile = userprofile

    if source != None:
      new_activity.source_id = source.id

    # ============================= [UserProfile Activities] =============================
    if activity == "ACTIVITY_ACCOUNT_CREATED":
      new_activity.text = "%s just joined EmergencyPetMatcher!" % (userprofile.user.username)
      new_activity.source_id = userprofile.id
      new_activity.activity = "ACTIVITY_ACCOUNT_CREATED"

    elif activity == "ACTIVITY_LOGIN":
      new_activity.text = "%s logged in to EPM." % (userprofile.user.username)           
      new_activity.source_id = userprofile.id
      new_activity.activity = "ACTIVITY_LOGIN"

    elif activity == "ACTIVITY_LOGOUT":
      new_activity.text = "%s logged out of EPM." % (userprofile.user.username)           
      new_activity.source_id = userprofile.id
      new_activity.activity = "ACTIVITY_LOGOUT"  

    elif activity == "ACTIVITY_USER_CHANGED_USERNAME":
      new_activity.text = "%s renamed his/her username." % (userprofile.user.username)           
      new_activity.source_id = userprofile.id
      new_activity.activity = "ACTIVITY_USER_CHANGED_USERNAME"      

    elif activity == "ACTIVITY_USER_SET_PHOTO":
      new_activity.text = "%s set a new profile picture." % (userprofile.user.username)           
      new_activity.source_id = userprofile.id
      new_activity.activity = "ACTIVITY_USER_SET_PHOTO"   

    elif activity == "ACTIVITY_SOCIAL_FOLLOW":
      new_activity.text = "%s is now following %s." % (userprofile.user.username, source.user.username)           
      new_activity.activity = "ACTIVITY_SOCIAL_FOLLOW"

    # ============================= [PetReport Activities] =============================
    elif activity == "ACTIVITY_PETREPORT_SUBMITTED":
      new_activity.text = "%s reported a %s %s named %s." % (userprofile.user.username, source.status, source.pet_type, source.pet_name)           
      new_activity.activity = "ACTIVITY_PETREPORT_SUBMITTED"       

    elif activity == "ACTIVITY_PETREPORT_ADD_BOOKMARK":
      new_activity.text = "%s bookmarked a %s %s named %s." % (userprofile.user.username, source.status, source.pet_type, source.pet_name)           
      new_activity.activity = "ACTIVITY_PETREPORT_ADD_BOOKMARK"        

    elif activity == "ACTIVITY_PETREPORT_REMOVE_BOOKMARK":
      new_activity.text = "%s removed a bookmark for a %s %s named %s." % (userprofile.user.username, source.status, source.pet_type, source.pet_name)           
      new_activity.activity = "ACTIVITY_PETREPORT_REMOVE_BOOKMARK"

    # ============================= [PetMatch Activities] =============================
    elif activity == "ACTIVITY_PETMATCH_PROPOSED":
      new_activity.text = "%s created a match with two %ss." % (userprofile.user.username, source.lost_pet.pet_type)           
      new_activity.activity = "ACTIVITY_PETMATCH_PROPOSED"

    elif activity == "ACTIVITY_PETMATCH_UPVOTE":
      new_activity.text = "%s voted on a match with two %ss." % (userprofile.user.username, source.lost_pet.pet_type)
      new_activity.activity = "ACTIVITY_PETMATCH_UPVOTE"

    elif activity == "ACTIVITY_PETMATCH_DOWNVOTE":
      new_activity.text = "%s voted on a match with two %ss." % (userprofile.user.username, source.lost_pet.pet_type)
      new_activity.activity = "ACTIVITY_PETMATCH_DOWNVOTE"

    # ============================= [PetCheck Activities] =============================
    elif activity == "ACTIVITY_PETCHECK_VERIFY":
      new_activity.text = "%s triggered pet checking for a match with two %ss." % (userprofile.user.username, source.lost_pet.pet_type)
      new_activity.activity = "ACTIVITY_PETCHECK_VERIFY"        

    elif activity == "ACTIVITY_PETCHECK_VERIFY_SUCCESS":
      lost_pet = source.petmatch.lost_pet

      if lost_pet.UserProfile_is_owner(userprofile) == True:
        new_activity.text = "%s has been reunited with %s %s named %s! Congratulations!" % (userprofile.user.username, 
                                                                                            lost_pet.status, 
                                                                                            lost_pet.pet_type, 
                                                                                            lost_pet.pet_name)
      else:
        new_activity.text = "%s has reunited a %s %s named %s with its original owner! Congratulations!" % (userprofile.user.username,
                                                                                                            lost_pet.status,
                                                                                                            lost_pet.pet_type,
                                                                                                            lost_pet.pet_name)
      new_activity.activity = "ACTIVITY_PETCHECK_VERIFY_SUCCESS" 

    elif activity == "ACTIVITY_PETCHECK_VERIFY_FAIL":
      new_activity.text = "Unfortunately, the match with %s and %s is not the right one. Keep trying!" % (source.petmatch.lost_pet.pet_name, 
                                                                                                              source.petmatch.found_pet.pet_name)
      new_activity.activity = "ACTIVITY_PETCHECK_VERIFY_FAIL" 

    else:
      print_error_msg("Activity Type %s is not supported." % activity)
      return None

    new_activity.save()
    return new_activity

  def __unicode__ (self):
    return '%s: ID{%s} %s' % (self.activity, self.id, self.text)



