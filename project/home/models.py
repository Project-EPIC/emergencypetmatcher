from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from utilities.utils import *
from constants import *
import pdb

#The Activity Object Model
class Activity(models.Model):
  userprofile = models.ForeignKey("socializing.UserProfile", null=False, default=None)
  source_id = models.IntegerField(null=False, default=None)
  activity = models.CharField(max_length=ACTIVITIES_MAX_LENGTH, choices=(zip(ACTIVITIES.keys(), ACTIVITIES.keys())), null=False, default=None)
  date_posted = models.DateTimeField(null=False, auto_now_add=True)
  text = models.CharField(max_length=150, null=False, default=None)

  def get_source_DICT(self):
    from socializing.models import UserProfile
    from reporting.models import PetReport
    from matching.models import PetMatch
    from verifying.models import PetReunion, PetMatchCheck

    try:
      if ACTIVITIES[self.activity]["source"] == "userprofile":
        source = UserProfile.objects.get(pk=self.source_id)
      elif ACTIVITIES[self.activity]["source"] == "petreport":
        source = PetReport.objects.get(pk=self.source_id)
      elif ACTIVITIES[self.activity]["source"] == "petmatch":
        source = PetMatch.objects.get(pk=self.source_id)
      elif ACTIVITIES[self.activity]["source"] == "petmatchcheck":
        source = PetMatchCheck.objects.get(pk=self.source_id)
      elif ACTIVITIES[self.activity]["source"] == "petreunion":
        source = PetReunion.objects.get(pk=self.source_id)
      else:
        return None
    except ObjectDoesNotExist:
      return None

    return source.to_DICT()

  @staticmethod
  def get_Activities_for_feed(page, since_date=None, userprofile=None):
    if since_date == None:
      since_date = datetime.strptime("9/1/2014", '%m/%d/%Y')
    
    #Build up the Activity Query by appending to this Q object.
    q_objects = Q()
    for activity in ACTIVITY_SOCIAL_ACTIVITIES:
      q_objects |= Q(activity=activity)

    activities = list(Activity.objects.filter(q_objects).order_by("id").reverse())
    return get_objects_by_page(activities, page, limit=NUM_ACTIVITIES_HOMEPAGE)

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
      new_activity.activity = "ACTIVITY_ACCOUNT_CREATED"
      new_activity.source_id = userprofile.id
      new_activity.text = "%s just joined EmergencyPetMatcher!" % (userprofile.user.username)
      
    elif activity == "ACTIVITY_LOGIN":
      new_activity.activity = "ACTIVITY_LOGIN"
      new_activity.source_id = userprofile.id
      new_activity.text = "%s logged in to EPM." % (userprofile.user.username)           

    elif activity == "ACTIVITY_LOGOUT":
      new_activity.activity = "ACTIVITY_LOGOUT"  
      new_activity.source_id = userprofile.id
      new_activity.text = "%s logged out of EPM." % (userprofile.user.username)           

    elif activity == "ACTIVITY_USER_CHANGED_USERNAME":
      new_activity.activity = "ACTIVITY_USER_CHANGED_USERNAME"      
      new_activity.source_id = userprofile.id
      new_activity.text = "%s renamed his/her username." % (userprofile.user.username)           

    elif activity == "ACTIVITY_USER_SET_PHOTO":
      new_activity.activity = "ACTIVITY_USER_SET_PHOTO"   
      new_activity.source_id = userprofile.id
      new_activity.text = "%s set a new profile picture." % (userprofile.user.username)           
      
    elif activity == "ACTIVITY_SOCIAL_FOLLOW":
      new_activity.activity = "ACTIVITY_SOCIAL_FOLLOW"
      new_activity.text = "%s is now following %s." % (userprofile.user.username, source.user.username)           

    elif activity == "ACTIVITY_SOCIAL_UNFOLLOW":
      new_activity.activity = "ACTIVITY_SOCIAL_UNFOLLOW"
      new_activity.text = "%s is no longer following %s." % (userprofile.user.username, source.user.username)                 

    elif activity == "ACTIVITY_SOCIAL_SEND_MESSAGE_TO_USER":
      new_activity.activity = "ACTIVITY_SOCIAL_SEND_MESSAGE_TO_USER"
      new_activity.text = "%s sent a message to %s." % (userprofile.user.username, source.user.username)                       

    # ============================= [PetReport Activities] =============================
    elif activity == "ACTIVITY_PETREPORT_SUBMITTED":
      new_activity.activity = "ACTIVITY_PETREPORT_SUBMITTED"    
      new_activity.text = "%s reported a %s %s named %s." % (userprofile.user.username, source.status, source.pet_type, source.pet_name)           
         
    elif activity == "ACTIVITY_PETREPORT_ADD_BOOKMARK":
      new_activity.activity = "ACTIVITY_PETREPORT_ADD_BOOKMARK"   
      new_activity.text = "%s bookmarked a %s %s named %s." % (userprofile.user.username, source.status, source.pet_type, source.pet_name)           
           
    elif activity == "ACTIVITY_PETREPORT_REMOVE_BOOKMARK":
      new_activity.activity = "ACTIVITY_PETREPORT_REMOVE_BOOKMARK"
      new_activity.text = "%s removed a bookmark for a %s %s named %s." % (userprofile.user.username, source.status, source.pet_type, source.pet_name)           
      
    # ============================= [PetMatch Activities] =============================
    elif activity == "ACTIVITY_PETMATCH_PROPOSED":
      new_activity.activity = "ACTIVITY_PETMATCH_PROPOSED"
      new_activity.text = "%s created a match with two %ss." % (userprofile.user.username, source.lost_pet.pet_type)           
      
    elif activity == "ACTIVITY_PETMATCH_UPVOTE":
      if Activity.objects.filter(source_id=source.id, userprofile=userprofile, activity=activity).exists() == True:
        return False
      new_activity.activity = "ACTIVITY_PETMATCH_UPVOTE"
      new_activity.text = "%s voted on a match with two %ss." % (userprofile.user.username, source.lost_pet.pet_type)
      
    elif activity == "ACTIVITY_PETMATCH_DOWNVOTE":
      if Activity.objects.filter(source_id=source.id, userprofile=userprofile, activity=activity).exists() == True:
        return False      
      new_activity.activity = "ACTIVITY_PETMATCH_DOWNVOTE"
      new_activity.text = "%s voted on a match with two %ss." % (userprofile.user.username, source.lost_pet.pet_type)
      
    # ============================= [PetMatchCheck Activities] =============================
    elif activity == "ACTIVITY_PETMATCHCHECK_VERIFY":
      new_activity.activity = "ACTIVITY_PETMATCHCHECK_VERIFY"    
      new_activity.text = "%s triggered pet match checking for a match with two %ss." % (userprofile.user.username, source.petmatch.lost_pet.pet_type)
          
    elif activity == "ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS":
      lost_pet = source.petmatch.lost_pet
      new_activity.activity = "ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS" 
      new_activity.text = "%s has reunited a %s %s named %s with its original owner! Congratulations!" % (userprofile.user.username, lost_pet.status, lost_pet.pet_type, lost_pet.pet_name)
    
    elif activity == "ACTIVITY_PETMATCHCHECK_VERIFY_FAIL":
      new_activity.activity = "ACTIVITY_PETMATCHCHECK_VERIFY_FAIL" 
      new_activity.text = "%s unfortunately didn't match %s with %s successfully. Keep trying!" % ( userprofile.user.username, source.petmatch.lost_pet.pet_name, source.petmatch.found_pet.pet_name)
    
  # ============================= [PetReunion Activities] =============================  
    elif activity == "ACTIVITY_PETREUNION_CREATED":
      new_activity.activity = "ACTIVITY_PETREUNION_CREATED"
      new_activity.text = "%s has closed the pet report for %s." % (userprofile.user.username, source.petreport.pet_name)

    else:
      print_error_msg("Activity Type %s is not supported." % activity)
      return None

    new_activity.save()
    return new_activity

  def __unicode__ (self):
    return '%s: ID{%s} %s' % (self.activity, self.id, self.text)



