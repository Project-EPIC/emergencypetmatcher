from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.forms import ModelForm, Textarea
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.validators import email_re
from django.core.files.storage import FileSystemStorage
from django import forms
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import now as datetime_now
from datetime import timedelta
from django.conf import settings
from django.core.files.images import ImageFile
from django.forms.models import model_to_dict
from constants import *
from PIL import Image
import os, time, datetime as DATETIME, simplejson, project.settings

'''===================================================================================
[models.py]: Models for the EPM system
==================================================================================='''

#The User Profile Model containing a 1-1 association with the 
#django.contrib.auth.models.User object, among other attributes.
class UserProfile (models.Model):
    '''Required Fields'''
    user = models.OneToOneField(User, null=False, default=None)    
    
    '''Non-Required Fields'''
    img_path = models.ImageField(upload_to='images/userprofile', default="images/userprofile/defaults/anonymous.gif", null=True)
    thumb_path = models.ImageField(upload_to='images/userprofile/thumbnails', default="images/userprofile/thumbnails/defaults/anonymous.gif", null=True)
    last_logout = models.DateTimeField(null=True, auto_now_add=True)
    following = models.ManyToManyField('self', null=True, symmetrical=False, related_name='followers')
    reputation = models.FloatField(default=0, null=True)
    # facebook_cred = models.CharField(max_length=100, null=True)
    # twitter_cred = models.CharField(max_length=100, null=True)
    #facebook_id = models.IntegerField(blank=True, null=True)
    #twitter_id = models.IntegerField(blank=True, null=True)
    # terms = models.BooleanField(default=False, NullBooleanField=True)

    #Create the activity log for this user
    def set_activity_log(self):
        print_success_msg("A new UserProfile log file was created for {%s} with ID{%d}\n" % (self.user.username, self.id))
        self.save()
        logger.log_activity(ACTIVITY_ACCOUNT_CREATED, self)    

    def send_email_message_to_UserProfile (self, target_userprofile, message, test_email=True):
        if email_re.match(target_userprofile.user.email) or (test_email == True):
            site = Site.objects.get(pk=1)
            ctx = {"site":site, "message":message, "from_user":self.user, "from_user_profile_URL": URL_USERPROFILE + str(self.id)}
            email_body = render_to_string(TEXTFILE_EMAIL_USERPROFILE_MESSAGE, ctx)
            email_subject = "EmergencyPetMatcher: You have a new message from %s" % self.user.username

            #If test_email, just return email properties - no need to email.
            if test_email == True:
                return {"subject": email_subject, "body":email_body, "from_username": self.user.username, "to_username": target_userprofile.user.username}

            #Go ahead and email now.
            target_userprofile.user.email_user(email_subject,email_body,from_email=None)
            return True
        return False        

    @staticmethod
    def get_UserProfile(profile_id=None, username=None):
        try:
            if username != None:
                existing_profile = UserProfile.objects.get(user__username=username)
            elif profile_id != None:
                existing_profile = UserProfile.objects.get(pk=profile_id)
            else:
                return None
            return existing_profile

        except UserProfile.DoesNotExist:
            return None        

    #Update the current user's reputation points based on an activity
    def update_reputation(self, activity):
        if activity == ACTIVITY_PETMATCH_UPVOTE:
            self.reputation += REWARD_PETMATCH_VOTE
        elif activity == ACTIVITY_PETMATCH_DOWNVOTE:
            self.reputation += REWARD_PETMATCH_VOTE
        elif activity == ACTIVITY_PETREPORT_SUBMITTED:
            self.reputation += REWARD_PETREPORT_SUBMIT
        elif activity == ACTIVITY_PETMATCH_PROPOSED:
            self.reputation += REWARD_PETMATCH_PROPOSE
        elif activity == ACTIVITY_USER_BEING_FOLLOWED:
            self.reputation += REWARD_USER_FOLLOWED
        elif activity == ACTIVITY_USER_BEING_UNFOLLOWED:
            self.reputation -= REWARD_USER_FOLLOWED
        elif activity == ACTIVITY_PETREPORT_ADD_BOOKMARK:
            self.reputation += REWARD_PETREPORT_BOOKMARK
        elif activity == ACTIVITY_PETREPORT_REMOVE_BOOKMARK:
            self.reputation -= REWARD_PETREPORT_BOOKMARK
        elif activity == ACTIVITY_ACCOUNT_CREATED:
            self.reputation += REWARD_NEW_ACCOUNT
        elif activity == ACTIVITY_USER_PROPOSED_PETMATCH_UPVOTE:
            self.reputation += REWARD_USER_PROPOSED_PETMATCH_VOTE
        elif activity == ACTIVITY_USER_PROPOSED_PETMATCH_SUCCESSFUL:
            self.reputation += REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL
        elif activity == ACTIVITY_USER_PROPOSED_PETMATCH_FAILURE:
            self.reputation += REWARD_USER_PROPOSED_PETMATCH_FAILURE
        elif activity == ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL:
            self.reputation += REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL
        elif activity == ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL:
            self.reputation += REWARD_PETMATCH_UPVOTE_SUCCESSFUL
        else:
            print_error_msg("Cannot update reputation points: This is not a valid activity!")
            return False

        #Save the UserProfile and return True
        self.save()
        return True

    #check if username exists in the database
    @staticmethod
    def username_exists(username):
        if User.objects.filter(username=username).count():
            return True
        return False            

    def __unicode__ (self):
         return '{ID{%s} %s}' % (self.id, self.user.username)


    #set_img_path(): Sets the image path and thumb path for this UserProfile. Save is optional.
    def set_images(self, img_path, save=True, rotation=0):
        #Deal with the 'None' case.
        if img_path == None:
            self.img_path = "images/userprofile/defaults/anonymous.gif"
            self.thumb_path = "images/userprofile/thumbnails/defaults/anonymous.gif"

            if save == True:
                self.save()
        else:
            #Safely open the image.
            img = open_image(img_path)

            if save == True:
                #Save first - we must have the UserProfile ID.
                self.img_path = None
                self.thumb_path = None
                self.save()

                #Make this unique to prevent any image overwrites when saving a picture for a UserProfile.
                unique_img_name = str(self.id) + "-" + self.user.username + ".jpg"

                #Perform rotation (if it applies)
                img = img.rotate(rotation)
                self.img_path = "images/userprofile/" + unique_img_name
                self.thumb_path = "images/userprofile/test/" + unique_img_name                    
                img.save(USERPROFILE_IMAGES_DIRECTORY + unique_img_name, "JPEG", quality=75)
                img.thumbnail((USERPROFILE_THUMBNAIL_WIDTH, USERPROFILE_THUMBNAIL_HEIGHT), Image.ANTIALIAS)
                img.save(USERPROFILE_THUMBNAILS_DIRECTORY + unique_img_name, "JPEG", quality=75)

                #Save again.
                self.save()

            else:
                self.img_path = img_path
                self.thumb_path = img_path         


class PetReport(models.Model):

    '''Required Fields'''
    #Type of Pet
    pet_type = models.CharField(max_length=PETREPORT_PET_TYPE_LENGTH, choices = PET_TYPE_CHOICES, null=False, default=None)
    #Status of Pet (Lost/Found)
    status = models.CharField(max_length = PETREPORT_STATUS_LENGTH, choices = STATUS_CHOICES, null=False, default=None)
    #Date Lost/Found
    date_lost_or_found = models.DateField(null=False)
    #The UserProfile who is submitting this PetReport (ForeignKey: Many-to-one relationship with User)
    proposed_by = models.ForeignKey('UserProfile', null=False, default=None, related_name='proposed_related')

    '''Non-Required Fields'''
    #Sex of the Pet
    sex = models.CharField(max_length=PETREPORT_SEX_LENGTH, choices=SEX_CHOICES, null=True)
    #Size of the Pet, in ranges
    size = models.CharField(max_length=PETREPORT_SIZE_LENGTH, choices=SIZE_CHOICES, null=True)
    #Location where found
    location = models.CharField(max_length=PETREPORT_LOCATION_LENGTH, null=True)
    #Lat/Long Geo-coordinates of Location
    geo_location_lat = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    geo_location_long = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    #Microchip ID of Pet
    microchip_id = models.CharField(max_length=PETREPORT_MICROCHIP_ID_LENGTH, null=True)
    #Pet Tag Information (if available)
    tag_info = models.CharField(max_length=PETREPORT_TAG_INFO_LENGTH, null=True, default="")
    #Contact Name of Person who is sheltering/reporting lost/found Pet (if different than proposed_by UserProfile)
    contact_name = models.CharField(max_length=PETREPORT_CONTACT_NAME_LENGTH, null=True)
    #Contact Phone Number of Person who is sheltering/reporting lost/found Pet (if different than proposed_by UserProfile)
    contact_number = models.CharField(max_length=PETREPORT_CONTACT_NUMBER_LENGTH, null=True)
    #Contact Email Address of Person who is sheltering/reporting lost/found Pet (if different than proposed_by UserProfile)
    contact_email = models.CharField(max_length=PETREPORT_CONTACT_EMAIL_LENGTH, null=True)        
    #Img of Pet
    img_path = models.ImageField(upload_to='images/petreport', null=True)
    #Thumbnail Img of Pet
    thumb_path = models.ImageField(upload_to="images/petreport/thumbnails", null=True)
    #Spayed or Neutered?
    spayed_or_neutered = models.CharField(max_length=PETREPORT_SPAYED_OR_NEUTERED_LENGTH, choices=SPAYED_OR_NEUTERED_CHOICES, null=True, default="Not Known")
    #Pet Name (if available)
    pet_name = models.CharField(max_length=PETREPORT_PET_NAME_LENGTH, null=True, default='unknown') 
    #Pet Age (if known/available)
    age = models.CharField(max_length=PETREPORT_AGE_LENGTH, null=True, choices=AGE_CHOICES,default="Not Known")
    #Color(s) of Pet
    color = models.CharField(max_length=PETREPORT_COLOR_LENGTH, null=True,default='unknown')
    #Breed of Pet
    breed = models.CharField(max_length=PETREPORT_BREED_LENGTH, null=True,default='unknown')
    #Description of Pet
    description   = models.CharField(max_length=PETREPORT_DESCRIPTION_LENGTH, null=True, default=" ")
    #The UserProfiles who are working on this PetReport (Many-to-Many relationship with User)
    workers = models.ManyToManyField('UserProfile', null=True, related_name='workers_related')
    #The UserProfiles who have bookmarked this PetReport
    bookmarked_by = models.ManyToManyField('UserProfile', null=True, related_name='bookmarks_related')
    #A pet report is closed once it has been successfully matched
    closed = models.BooleanField(default=False)
    revision_number = models.IntegerField(null=True) #update revision using view

    #Override the save method for this model
    def save(self, *args, **kwargs):
        #Take care of defaults.
        if self.pet_name == None or self.pet_name.strip() == "":
            self.pet_name = "unknown"

        super(PetReport, self).save(args, kwargs) 
        print_success_msg ("{%s} has been saved by %s!" % (self, self.proposed_by))           
        return self

    ''' Determine if the input UserProfile (user) has bookmarked this PetReport already '''
    def UserProfile_has_bookmarked(self, user_profile):
        assert isinstance(user_profile, UserProfile)
        try:
            user = self.bookmarked_by.get(pk = user_profile.id)
        except UserProfile.DoesNotExist:
            user = None        
        if (user != None):
            return True
        else:
            return False
        return False

    '''this function compares 6 attributes of both pets and returns the number of matching attributes.
    the attributes compared are: age, sex, size, spayed_or_neutered, pet_name, and breed'''
    def compare(self, petreport):
        assert isinstance (petreport, PetReport)
        matching_attrs = 0

        #Sex
        if self.sex == petreport.sex:
            matching_attrs += 1
        #Size
        if self.size == petreport.size:
            matching_attrs += 1
        #Spayed/Neutered
        if self.spayed_or_neutered == petreport.spayed_or_neutered:
            matching_attrs += 1
        #Pet Name
        if self.pet_name.lower() == petreport.pet_name.lower():
            matching_attrs += 1
        #Breed
        if self.breed.lower() == petreport.breed.lower():
            matching_attrs += 1
        #Age
        if self.age == petreport.age:
            matching_attrs += 1

        return matching_attrs        
    
    #set_img_path(): Sets the image path and thumb path for this PetReport. Save is optional.
    def set_images(self, img_path, save=True, rotation=0):
        #Deal with the 'None' case.
        if img_path == None:
            if self.pet_type == PETREPORT_PET_TYPE_DOG:
                self.img_path = "images/petreport/defaults/dog_silhouette.jpg"
                self.thumb_path = "images/petreport/thumbnails/defaults/dog_silhouette.jpg"
            elif self.pet_type == PETREPORT_PET_TYPE_CAT:
                self.img_path = "images/petreport/defaults/cat_silhouette.jpg"
                self.thumb_path = "images/petreport/thumbnails/defaults/cat_silhouette.jpg"
            elif self.pet_type == PETREPORT_PET_TYPE_BIRD:
                self.img_path = "images/petreport/defaults/bird_silhouette.jpg"                    
                self.thumb_path = "images/petreport/thumbnails/defaults/bird_silhouette.jpg"
            elif self.pet_type == PETREPORT_PET_TYPE_HORSE:
                self.img_path = "images/petreport/defaults/horse_silhouette.jpg"
                self.thumb_path = "images/petreport/thumbnails/defaults/horse_silhouette.jpg"
            elif self.pet_type == PETREPORT_PET_TYPE_RABBIT:
                self.img_path = "images/petreport/defaults/rabbit_silhouette.jpg"
                self.thumb_path = "images/petreport/thumbnails/defaults/rabbit_silhouette.jpg"
            elif self.pet_type == PETREPORT_PET_TYPE_SNAKE:
                self.img_path = "images/petreport/defaults/snake_silhouette.jpg"                                       
                self.thumb_path = "images/petreport/thumbnails/defaults/snake_silhouette.jpg"
            elif self.pet_type == PETREPORT_PET_TYPE_TURTLE:
                self.img_path = "images/petreport/defaults/turtle_silhouette.jpg"
                self.thumb_path = "images/petreport/thumbnails/defaults/turtle_silhouette.jpg"
            else:
                self.img_path = "images/petreport/defaults/other_silhouette.jpg"
                self.thumb_path = "images/petreport/thumbnails/defaults/other_silhouette.jpg"

            if save == True:
                self.save()
        else:
            #Safely open the image.
            img = open_image(img_path)

            if save == True:
                #Save first - we must have the PetReport ID
                self.img_path = None
                self.thumb_path = None
                self.save()

                #Make this unique to prevent any image overwrites when saving a picture for a PetReport.
                unique_img_name = str(self.proposed_by.id) + "-" + self.proposed_by.user.username + "-" + str(self.id) + "-" + self.pet_name + "-" + self.status + ".jpg"

                #Perform rotation (if it applies)
                img = img.rotate(rotation)
                self.img_path = "images/petreport/" + unique_img_name
                self.thumb_path = "images/petreport/thumbnails/" + unique_img_name
                img.save(PETREPORT_IMAGES_DIRECTORY + unique_img_name, "JPEG", quality=75)
                img.thumbnail((PETREPORT_THUMBNAIL_WIDTH, PETREPORT_THUMBNAIL_HEIGHT), Image.ANTIALIAS)
                img.save(PETREPORT_THUMBNAILS_DIRECTORY + unique_img_name, "JPEG", quality=75)

                #Save again.
                self.save()

            else:
                self.img_path = img_path
                self.thumb_path = img_path

        
    @staticmethod
    def get_PetReport(status, pet_type, pet_name=None, petreport_id=None):
        try:
            if petreport_id != None:
                existing_pet = PetReport.objects.get(pk=petreport_id)
            elif pet_name != None:
                existing_pet = PetReport.objects.get(status=status, pet_type=pet_type, pet_name=pet_name)
            else:
                existing_pet = PetReport.objects.get(status=status, pet_type=pet_type)

            return existing_pet

        except PetReport.DoesNotExist:
            return None

    @staticmethod
    def get_PetReports_by_page(filtered_petreports, page):
        if (page != None and page > 0):
            page = int(page)
            filtered_petreports = filtered_petreports [((page-1) * NUM_PETREPORTS_HOMEPAGE):((page-1) * NUM_PETREPORTS_HOMEPAGE + NUM_PETREPORTS_HOMEPAGE)]

        #Just return the list of PetReports.
        return filtered_petreports

    #Return a list of candidate PetReports that could potentially be matches for this PetReport.
    def get_candidate_PetReports(self):
        candidates = PetReport.objects.exclude(status = self.status).filter(pet_type = self.pet_type, closed=False)

        if len(candidates) == 0:
            return None
        return candidates

    #This method returns a ranked list of all PetReports found in the input specified list. This ranking is based on the PetReport compare() method.
    def get_ranked_PetReports(self, candidates, page=None):
        #Begin criteria ranking process: Rank based on how many similar PetReport features occur between target and candidate.
        results = []
        matches = {"match6":[], "match5":[],"match4":[],"match3":[],"match2":[],"match1":[],"match0":[]}

        for candidate in candidates:
            num_attributes_matched = self.compare(candidate)
            matches["match" + str(num_attributes_matched)].append(candidate)

        #Finally, feed the keys in the order of rank to a new PetReports list.
        for key in matches.keys():
            results += matches[key]             

        return self.get_PetReports_by_page (results, page)

    #Determine if the input UserProfile (user) is a worker for this PetReport.
    def UserProfile_is_worker(self, user_profile):
        assert isinstance(user_profile, UserProfile)
        try:
            worker = self.workers.get(pk = user_profile.id)
            return True
        except UserProfile.DoesNotExist:
            return False

    def has_image(self):
        if self.img_path == None:
            return False
        return True

    def __unicode__(self):
        return '{ID{%s} %s %s name:%s}' % (self.id, self.status, self.pet_type, self.pet_name)

    def long_unicode (self):
        str = "PetReport {\n\tpet_type: %s\n\tstatus: %s\n\tproposed_by: %s\n\t" % (self.pet_type, self.status, self.proposed_by)
        str += "date_lost_or_found: %s\n\tsex: %s\n\tsize: %s\n\tlocation: %s\n\t" % (self.date_lost_or_found, self.sex, self.size, self.location)
        str += "age: %s\n\tbreed: %s\n\tdescription: %s\n\t}" % (self.age, self.breed, self.description)
        return str

    def convert_date_to_string(self):
        string = str(self.date_lost_or_found)
        return str

    def toDICT(self):
        #A customized version of django model function "model_to_dict"
        #to convert a PetReport model object to a dictionary object
        modeldict = model_to_dict(self)
        #Iterate through all fields in the model_dict
        for field in modeldict:
            value = modeldict[field]
            if isinstance(value, DATETIME.datetime) or isinstance(value, DATETIME.date):
                modeldict[field] = value.strftime("%B %d, %Y")
            elif isinstance(value, ImageFile):
                modeldict[field] = value.name
            elif field == "sex":
                modeldict[field] = self.get_sex_display()
            elif field == "size":
                modeldict[field] = self.get_size_display()
            elif field == "geo_location_lat" and str(value).strip() == "":
                modeldict[field] = None
            elif field == "geo_location_long" and str(value).strip() == "":
                modeldict[field] = None
        #Just add a couple of nice attributes.
        modeldict ["proposed_by_username"] = self.proposed_by.user.username       
        return modeldict

    def toJSON(self):
        #Convert a PetReport model object to a json object
        json = simplejson.dumps(self.toDICT())
        #print_info_msg("toJSON: " + str(json))
        return json


#The Pet Match Object Model
class PetMatch(models.Model):
    '''Required Fields'''
    #Lost Pet
    lost_pet = models.ForeignKey('PetReport', null=False, default=None, related_name='lost_pet_related')
    #Found Pet
    found_pet = models.ForeignKey('PetReport', null=False, default=None, related_name='found_pet_related')
    #UserProfile who proposed the PetMatch object.
    proposed_by = models.ForeignKey('UserProfile', null=False, related_name='proposed_by_related')
    #Date when PetMatch was proposed (created).
    proposed_date = models.DateTimeField(null=False, auto_now_add=True)
    #Description of PetMatch.
    '''Non-Required Fields'''
    description = models.CharField(max_length=PETMATCH_DESCRIPTION_LENGTH, null=True, default="")
    #is_open will be set to False once it is triggered for verification i.e., it will not be available
    #to the crowd for viewing/voting after this petmatch triggers the verification workflow or if it is 
    #declared as a Failed PetMatch when a successful PetMatch is found for either of the PetReports associated with
    #the current Petmatch instance.
    is_open = models.BooleanField(default=True)
    is_successful = models.BooleanField(default=False)
    #verification_triggered will be set to true if and when a PetMatch reaches the threshold for verification
    verification_triggered = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    #closed_by = models.ForeignKey('UserProfile', null=True, related_name='closed_by_related')
    #closed_date is the date when the PetMatch is closed for good (after verification)
    closed_date = models.DateTimeField(null=True)
    up_votes = models.ManyToManyField('UserProfile', null=True, related_name='up_votes_related')
    down_votes = models.ManyToManyField('UserProfile', null=True, related_name='down_votes_related')
    #verification_votes represents user responses sent via the verify_petmatch webpage.
    #the first bit holds the Lost Contact's response and the second bit holds the 
    #Found Contact's response. 
    #0 - No response was recorded
    #1 - user clicked on Yes
    #2 - User clicked on No
    verification_votes = models.CharField(max_length=PETMATCH_VERIFICATION_VOTES_LENGTH,default='00')

    '''Because of the Uniqueness constraint that the PetMatch must uphold, we override the save method'''
    def save(self, *args, **kwargs):
        #First, try to find an existing PetMatch
        lost_pet = self.lost_pet
        found_pet = self.found_pet
        
        #PetMatch inserted improperly
        if (lost_pet.status != "Lost") or (found_pet.status != "Found"):
            print_error_msg ("The PetMatch was not saved because it was inserted improperly. Check to make sure that the PetMatch consists of one lost and found pet and that they are being assigned to the lost and found fields, respectively.")
            return (None, PETMATCH_OUTCOME_INSERTED_IMPROPERLY)

        existing_match = PetMatch.get_PetMatch(self.lost_pet, self.found_pet)            

        #A PetMatch with the same lost and found pets (and same user who proposed it) already exists - SQL Update
        if existing_match != None:
            if existing_match.id == self.id:
                super(PetMatch, self).save(args, kwargs)
                print_info_msg ("[SQL UPDATE]: %s" % self)
                return (self, PETMATCH_OUTCOME_UPDATE)
            else:
                print_info_msg ("[DUPLICATE PETMATCH]: %s VS. %s" % (self, existing_match))
                return (None, PETMATCH_OUTCOME_DUPLICATE_PETMATCH) #Duplicate PetMatch!

        #Good to go: Save the PetMatch Object.
        super(PetMatch, self).save(*args, **kwargs)
        print_success_msg("PetMatch %s was saved!" % self)
        return (self, PETMATCH_OUTCOME_NEW_PETMATCH)


    ''' Determine if a PetMatch exists between pr1 and pr2, and if so, return it. Otherwise, return None. '''
    @staticmethod
    def get_PetMatch(pr1, pr2):
        assert isinstance(pr1, PetReport)
        assert isinstance(pr2, PetReport)

        try:
            if pr1.status == "Lost":
                existing_match = PetMatch.objects.get(lost_pet = pr1, found_pet = pr2)
            else:
                existing_match = PetMatch.objects.get(lost_pet = pr2, found_pet = pr1)

            return existing_match

        except PetMatch.DoesNotExist:
            return None

    ''' Determine if the input UserProfile (user) has up/down-voted on this PetMatch already '''
    def UserProfile_has_voted(self, user_profile):
        assert isinstance(user_profile, UserProfile)

        try:
            upvote = self.up_votes.get(pk = user_profile.id)
        except UserProfile.DoesNotExist:
            upvote = None
        try:
            downvote = self.down_votes.get(pk = user_profile.id)
        except UserProfile.DoesNotExist:
            downvote = None

        if (upvote != None):
            return UPVOTE
        elif (downvote != None):
            return DOWNVOTE
        return False  

    def toDICT(self):
        modeldict = model_to_dict(self)
        #Iterate through all fields in the model_dict
        for field in modeldict:
            value = modeldict[field]
            if isinstance(value, DATETIME.datetime) or isinstance(value, DATETIME.date):
                modeldict[field] = value.strftime("%B %d, %Y")
            elif isinstance(value, ImageFile):
                modeldict[field] = value.name
        #Just add a couple of nice attributes.
        modeldict ["proposed_by_username"] = self.proposed_by.user.username       
        return modeldict

    def toJSON(self):
        json = simplejson.dumps(self.toDICT())
        return json        

    def PetMatch_has_reached_threshold(self):
        #Difference (D) is calculated as the difference between number of upvotes and downvotes.
        #For a PetMatch to be successful, it should satisfy certain constraints. D should exceed a threshold value.
        difference = abs(self.up_votes.count() - self.down_votes.count())

        #Temporary: If the PetMatch proposer votes on this, and his/her vote is the only vote for this, then verification is triggered.
        if self.up_votes.count() == 1:
            if self.proposed_by == self.up_votes.all()[0] and (self.proposed_by == self.lost_pet.proposed_by or self.proposed_by == self.found_pet.proposed_by):
                return True

        if difference >= PETMATCH_THRESHOLD:
            return True
        else:
            return False

    #Change this to verify_PetMatch
    def verify_petmatch(self):
        self.is_open = False
        self.verification_triggered = True
        print_info_msg("Verification Triggered: PetMatch is now closed to the crowd.")
        petmatch_owner = self.proposed_by
        lost_pet_contact = self.lost_pet.proposed_by
        found_pet_contact = self.found_pet.proposed_by

        #Grab the Site object for the context variables
        site = Site.objects.get(pk=1)

        #If the PetMatch proposer is either the lost or found pet contact...
        if (petmatch_owner.id == lost_pet_contact.id) or (petmatch_owner.id == found_pet_contact.id): 
            Optionally_discuss_with_digital_volunteer = ""
        else:
            Optionally_discuss_with_digital_volunteer = "You may also discuss this pet match with %s, the digital volunteer who proposed this pet match. You can reach %s at %s" % (petmatch_owner.user.username, petmatch_owner.user.username, petmatch_owner.user.email)

        #Emails are sent to both parties iff all email addresses are valid (i.e. not test emails)
        if email_re.match(lost_pet_contact.user.email) and email_re.match(found_pet_contact.user.email) and email_re.match(petmatch_owner.user.email):
            ctx = { "site":site, 
                    "petmatch_id":self.id,
                    'pet_type':'your lost pet', 
                    'opposite_pet_type_contact':found_pet_contact.user.username, 
                    'pet_status':"found", 
                    'Optionally_discuss_with_digital_volunteer':Optionally_discuss_with_digital_volunteer }
            
            email_body = render_to_string(TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH, ctx)
            email_subject = EMAIL_SUBJECT_PETOWNER_VERIFY_PETMATCH
            lost_pet_contact.user.email_user(email_subject, email_body, from_email=None)            

            ctx.update({"pet_type": "the pet you found", 
                        "opposite_pet_type_contact": lost_pet_contact.user.username, 
                        "pet_status":"lost", 
                        "Optionally_discuss_with_digital_volunteer": Optionally_discuss_with_digital_volunteer})

            email_body = render_to_string(TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH, ctx)
            found_pet_contact.user.email_user(email_subject, email_body, from_email=None)

            #If the pet match was proposed by a person other than the lost_pet_contact/found_pet_contact, an email will be sent to this person as well.
            if Optionally_discuss_with_digital_volunteer != "":
                ctx = { 'lost_pet_contact':lost_pet_contact,'found_pet_contact':found_pet_contact }
                email_body = render_to_string(TEXTFILE_EMAIL_PETMATCH_PROPOSER, ctx)
                email_subject =  EMAIL_SUBJECT_PETMATCH_PROPOSER  
                petmatch_owner.user.email_user(email_subject,email_body,from_email=None)

            #Save after successfully sending off pet contact emails.
            self.save()
            
    def close_PetMatch(self):
        petmatch_owner = self.proposed_by
        lost_pet_contact = self.lost_pet.proposed_by
        found_pet_contact = self.found_pet.proposed_by

        if '0' not in self.verification_votes:
            self.closed_date = datetime_now()         
            '''If the PetMatch is successful, all related PetMatches will be closed 
            and is_successful is set to True'''
            if self.verification_votes == '11':
                self.is_successful = True

                for petmatch in self.lost_pet.lost_pet_related.all(): 
                    petmatch.is_open = False
                    petmatch.closed_date = datetime_now()
                    petmatch.save()
                for petmatch in self.found_pet.found_pet_related.all():
                    petmatch.is_open = False
                    petmatch.closed_date = datetime_now()
                    petmatch.save()

                #the lost and found pet reports for the pet match are closed
                petmatch.lost_pet.closed = True
                petmatch.lost_pet.save()
                petmatch.found_pet.closed = True
                petmatch.found_pet.save()
                
                # --------Reputation points--------
                # update reputation points for the following users:
                # petmatch_owner, lost_pet_contact, and found_pet_contact
                print_info_msg ("PetMatch Verification was a SUCCESS!")
                # Must to update reputation points twice since if updating petmatch_owner and lost_pet_contact
                # separately for the same user doesn't work
                if petmatch_owner.id == lost_pet_contact.id:
                    petmatch_owner.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_SUCCESSFUL)
                    petmatch_owner.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
                    found_pet_contact.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
                # Must to update reputation points twice since if updating petmatch_owner and found_pet_contact
                # separately for the same user doesn't work
                elif petmatch_owner.id == found_pet_contact.id:
                    petmatch_owner.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_SUCCESSFUL)
                    petmatch_owner.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
                    lost_pet_contact.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
                else:
                    petmatch_owner.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_SUCCESSFUL)
                    lost_pet_contact.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
                    found_pet_contact.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
                 # update reputation points for upvoters
                for upvoters in self.up_votes.all():
                    upvoters.update_reputation(ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL)
                # Must update reputation manually for petmatch_owner if found in the up_votes list because
                # the user is not updated in the previous for loop
                if petmatch_owner in self.up_votes.all():
                    petmatch_owner.update_reputation(ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL)
                # Must update reputation manually for lost_pet_contact if found in the up_votes list because
                # the user is not updated in the previous for loop
                elif lost_pet_contact in self.up_votes.all():
                    lost_pet_contact.update_reputation(ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL)
                # Must update reputation manually for ound_pet_contact if found in the up_votes list because
                # the user is not updated in the previous for loop
                elif found_pet_contact in self.up_votes.all():
                    found_pet_contact.update_reputation(ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL)
            else: 
                # if self.verification_votes == '22' or self.verification_votes == '12' or self.verification_votes == '21':
                    print_info_msg ("PetMatch Verification was NOT a success!")
                    petmatch_owner.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_FAILURE)

            self.save()    
            print_info_msg ("PetMatch %s has been closed" % (self))
    
    def __unicode__ (self):
        return '{ID{%s} lost:%s, found:%s, proposed_by:%s}' % (self.id, self.lost_pet, self.found_pet, self.proposed_by)


''' ============================ [FORM MODELS] ==================================== '''
''' These Models nicely organize the model-related data into Django Form objects that 
    have built-in validation functionality and can be passed around via POST requests. 
    Order of Fields matter.                                                         '''

#The PetReport ModelForm
class PetReportForm (ModelForm):

    '''Required Fields'''
    pet_type = forms.ChoiceField(label = 'Pet Type *', choices = PET_TYPE_CHOICES, required = True)
    status = forms.ChoiceField(label = "Pet Status *", help_text="(Lost/Found)", choices = STATUS_CHOICES, required = True)
    date_lost_or_found = forms.DateField(label = "Date Lost/Found *", widget = forms.DateInput, required = True)

    '''Non-Required Fields'''
    sex = forms.ChoiceField(label = "Sex", choices = SEX_CHOICES, required = False)
    size = forms.ChoiceField(label = "Size of Pet", choices = SIZE_CHOICES, required = False)
    location = forms.CharField(label = "Location", help_text="(Location where pet was lost/found)", max_length = PETREPORT_LOCATION_LENGTH , required = False)
    geo_location_lat = forms.DecimalField(label = "Geo Location Lat", help_text="(Lattitude coordinate)", max_digits=8, decimal_places=5, widget=forms.TextInput(attrs={'size':'10'}), initial=None, required=False)
    geo_location_long = forms.DecimalField(label = "Geo Location Long", help_text="(Longitude coordinate)", max_digits=8, decimal_places=5, widget=forms.TextInput(attrs={'size':'10'}),  initial=None, required=False)
    microchip_id = forms.CharField(label = "Microchip ID", max_length = PETREPORT_MICROCHIP_ID_LENGTH, required=False)
    tag_info = forms.CharField(label = "Tag and Collar Information", help_text="(if available)", max_length = PETREPORT_TAG_INFO_LENGTH, required=False, widget=Textarea)
    contact_name = forms.CharField(label = "Contact Name", max_length=PETREPORT_CONTACT_NAME_LENGTH, required=False)
    contact_number = forms.CharField(label = "Contact Phone Number", max_length=PETREPORT_CONTACT_NUMBER_LENGTH, required=False)
    contact_email = forms.CharField(label = "Contact Email Address", max_length=PETREPORT_CONTACT_EMAIL_LENGTH, required=False)
    img_path = forms.ImageField(label = "Upload an Image", help_text="(*.jpg, *.png, *.bmp), 3MB maximum", widget = forms.ClearableFileInput, required = False)
    spayed_or_neutered = forms.ChoiceField(label="Spayed/Neutered", choices=SPAYED_OR_NEUTERED_CHOICES, required=False)    
    pet_name = forms.CharField(label = "Pet Name", max_length=PETREPORT_PET_NAME_LENGTH, required = False) 
    age = forms.ChoiceField(label = "Age", choices=AGE_CHOICES,required = False)
    breed = forms.CharField(label = "Breed", max_length = PETREPORT_BREED_LENGTH, required = False)
    color = forms.CharField(label = "Coat Color(s)", max_length = PETREPORT_COLOR_LENGTH, required = False)
    description  = forms.CharField(label = "Pet Description", help_text="(Please describe the pet as accurately as possible)", max_length = PETREPORT_DESCRIPTION_LENGTH, widget = forms.Textarea, required = False)

    class Meta:
        model = PetReport
        exclude = ('revision_number', 'workers', 'proposed_by','bookmarked_by','closed', 'thumb_path')

#The UserProfile Form - used for editing the user profile
#edit initial value of each field either in the view or in the template
class UserProfileForm (forms.Form):
    #Required Fields
    username = forms.CharField(label="Username*",max_length=30) 

    #Non-Required Fields
    first_name = forms.CharField(label="First Name",max_length=30,required=False)
    last_name = forms.CharField(label="Last Name",max_length=30,required=False)
    email = forms.EmailField(label="Email*",required=False)
    old_password = forms.CharField(label="Old Password",max_length=30,widget = forms.PasswordInput,required=False) 
    new_password = forms.CharField(label="New Password",max_length=30,widget = forms.PasswordInput,required=False) 
    confirm_password = forms.CharField(label="Confirm Password",max_length=30,widget = forms.PasswordInput,required=False) 
    photo = forms.ImageField(label="Profile Picture", required=False)


class EditUserProfile(models.Model):
    user = models.OneToOneField(User,null=False,default=None)
    activation_key = models.CharField(max_length=40,null=True)
    date_of_change = models.DateTimeField(default=timezone.now)
    new_email = models.EmailField(null=True)
    def activation_key_expired(self):
        """ADAPTED FROM DJANGO-REGISTRATION: https://bitbucket.org/ubernostrum/django-registration

        Determine whether this activation key has expired, 
        returning a boolean -- ``True`` if the key
        has expired.
        
        Key expiration is determined by a two-step process:
        
        1. If the user has already activated his new email, 
           the key will have been reset to the string constant 
           ``ACTIVATED``. Re-activating is not permitted, and so 
           this method returns ``True`` in this case.

        2. Otherwise, the date the user changed his email is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after change of email during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        
        """
        expiration_date = timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == "ACTIVATED" or (self.date_of_change + expiration_date <= datetime_now())
    activation_key_expired.boolean = True

''' ============================ [SIGNALS] ==================================== '''

#Create a pre-delete signal function to delete a UserProfile before a User/UserProfile is deleted
@receiver (pre_delete, sender=UserProfile)
def delete_UserProfile(sender, instance=None, **kwargs):
    if instance.user == None:
        print_error_msg("User was deleted before UserProfile. Cannot delete log file.")
    else:    
        #Delete the UserProfile log file.
        logger.delete_log(instance)
        #Instead of deleting the User (which might break foreign-key relationships),
        #set the active flag to False (INACTIVE)
        instance.user.is_active = False
        instance.user.save()

#Create a post save signal function to setup a UserProfile when a User is created
@receiver (post_save, sender=User)
def setup_UserProfile(sender, instance, created, **kwargs):
    if created == True:
        #Create a UserProfile object.
        userprofile = UserProfile.objects.create(user=instance)
        userprofile.set_activity_log()
        userprofile.update_reputation(ACTIVITY_ACCOUNT_CREATED)

    elif instance.is_active:
        if logger.log_exists(instance.get_profile()) == False:
            logger.log_activity(ACTIVITY_ACCOUNT_CREATED, instance.get_profile())

#Post Add Signal function to check if a PetMatch has reached threshold
@receiver(m2m_changed, sender=PetMatch.up_votes.through)
def trigger_PetMatch_verification(sender, instance, action,**kwargs):
    #Checking condition that will return true once PetMatch reaches a threshold value,
    #if it returns true, pet match verification work flow is triggered.
    #print_debug_msg("PetMatch Verification Signal (Upvotes) TRIGGERED: %s" % action)
    if action == 'post_add':
        if instance.PetMatch_has_reached_threshold() == True:
            instance.verify_petmatch()



''' Import statements placed at the bottom of the page to prevent circular import dependence '''
import logger
from utils import print_info_msg, print_error_msg, print_debug_msg, print_success_msg, open_image








