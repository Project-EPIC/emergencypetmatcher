from django.db import models
from reporting.models import PetReport
from social.models import UserProfile
from utilities.utils import *
from verifying.contants import *
from constants import *

#The Pet Match Object Model
class PetMatch(models.Model):
    '''Required Fields'''
    #Lost Pet
    lost_pet = models.ForeignKey(PetReport, null=False, default=None, related_name='lost_pet_related')
    #Found Pet
    found_pet = models.ForeignKey(PetReport, null=False, default=None, related_name='found_pet_related')
    #UserProfile who proposed the PetMatch object.
    proposed_by = models.ForeignKey(UserProfile, null=False, related_name='proposed_by_related')
    #Date when PetMatch was proposed (created).
    proposed_date = models.DateTimeField(null=False, auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    up_votes = models.ManyToManyField(UserProfile, null=True, related_name='up_votes_related')
    down_votes = models.ManyToManyField(UserProfile, null=True, related_name='down_votes_related')

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

    @staticmethod
    def get_PetMatches_by_page(filtered_petmatches, page):
        if (page != None and page > 0):
            page = int(page)
            filtered_petmatches = filtered_petmatches [((page-1) * NUM_PETMATCHES_HOMEPAGE):((page-1) * NUM_PETMATCHES_HOMEPAGE + NUM_PETMATCHES_HOMEPAGE)]
            
        #Just return the list of PetReports.
        return filtered_petmatches



    # Determine (return UPVOTE/DOWNVOTE) if the input UserProfile (user) has up/down-voted on this PetMatch already
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
        lost_pet_contact = self.lost_pet.proposed_by
        found_pet_contact = self.found_pet.proposed_by
        petmatch_owner = self.proposed_by

        #Temporary: If the PetMatch proposer votes on this match and is the only vote for it, and he/she happens to be either the lost or found pet submitter,
        #AND if all email addresses are valid for these contacts, then verification is triggered.
        if self.up_votes.count() == 1 and (self.proposed_by == self.up_votes.all()[0]):
            if (self.proposed_by == lost_pet_contact or self.proposed_by == found_pet_contact) and email_is_valid(lost_pet_contact.user.email) and email_is_valid(found_pet_contact.user.email) and email_is_valid(petmatch_owner.user.email):
                return True

        if difference >= VERIFICATION_DEFAULT_THRESHOLD:
            return True
        else:
            return False

    
    def __unicode__ (self):
        return '{ID{%s} lost:%s, found:%s, proposed_by:%s}' % (self.id, self.lost_pet, self.found_pet, self.proposed_by)
