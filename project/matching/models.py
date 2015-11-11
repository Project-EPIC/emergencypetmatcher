from django.db import models
from socializing.models import UserProfile
from reporting.models import PetReport, PetReportForm
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from utilities.utils import *
from constants import *
from verifying.constants import *
import json, pdb

#The Pet Match Object Model
class PetMatch(models.Model):
    lost_pet = models.ForeignKey("reporting.PetReport", null=False, default=None, related_name='lost_pet_related')
    found_pet = models.ForeignKey("reporting.PetReport", null=False, default=None, related_name='found_pet_related')
    #UserProfile who proposed the PetMatch object.
    proposed_by = models.ForeignKey("socializing.UserProfile", null=False, related_name='proposed_by_related')
    #Date when PetMatch was proposed (created).
    proposed_date = models.DateTimeField(null=False, auto_now_add=True)
    #Field to capture failed PetMatches.
    has_failed = models.BooleanField(null=False, default=False)
    up_votes = models.ManyToManyField("socializing.UserProfile", related_name='up_votes_related')
    down_votes = models.ManyToManyField("socializing.UserProfile", related_name='down_votes_related')

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

    def to_DICT(self):
        return {
            "id"                    : self.id,
            "lost_pet_name"         : self.lost_pet.pet_name,
            "lost_pet_type"         : self.lost_pet.pet_type,
            "lost_pet_breed"        : self.lost_pet.breed,
            "found_pet_name"        : self.found_pet.pet_name,
            "found_pet_type"        : self.found_pet.pet_type,
            "found_pet_breed"       : self.found_pet.breed,
            "img_path"              : [self.lost_pet.img_path.name, self.found_pet.img_path.name],
            "thumb_path"            : [self.lost_pet.thumb_path.name, self.found_pet.thumb_path.name],
            "proposed_by_username"  : self.proposed_by.user.username,
            "proposed_by_id"        : self.proposed_by.id,
            "proposed_date"         : self.proposed_date.ctime(),
            "has_failed"            : self.has_failed,
            "is_successful"         : self.is_successful(),
            "num_upvotes"           : self.up_votes.count(),
            "num_downvotes"         : self.down_votes.count()
        }

    def get_display_fields(self):
        return [
            {"attr": "pet_name", "label": "Pet Name", "lost_pet_value": self.lost_pet.pet_name, "found_pet_value": self.found_pet.pet_name},
            {"attr": "pet_type", "label": "Pet Type", "lost_pet_value": self.lost_pet.pet_type, "found_pet_value": self.found_pet.pet_type},
            {"attr": "status", "label": "Lost/Found", "lost_pet_value": self.lost_pet.status, "found_pet_value": self.found_pet.status},
            {"attr": "date_lost_or_found", "label": "Date Lost/Found", "lost_pet_value": self.lost_pet.date_lost_or_found.strftime("%B %d, %Y"), "found_pet_value": self.found_pet.date_lost_or_found.strftime("%B %d, %Y")},
            {"attr": "proposed_by_username", "label": "Contact", "lost_pet_value": self.lost_pet.proposed_by.user.username, "found_pet_value": self.found_pet.proposed_by.user.username},
            {"attr": "event_tag", "label":"Event Tag", "lost_pet_value": self.lost_pet.event_tag, "found_pet_value": self.found_pet.event_tag},
            {"attr": "location", "label": "Location", "lost_pet_value": self.lost_pet.location, "found_pet_value": self.found_pet.location},
            {"attr": "microchip_id", "label": "Microchipped?", "lost_pet_value": "Yes" if (self.lost_pet.microchip_id != "") else "No", "found_pet_value": "Yes" if (self.found_pet.microchip_id != "") else "No"},
            {"attr": "spayed_or_neutered", "label": "Spayed/Neutered", "lost_pet_value": self.lost_pet.spayed_or_neutered, "found_pet_value": self.found_pet.spayed_or_neutered},
            {"attr": "age", "label": "Age", "lost_pet_value": self.lost_pet.age, "found_pet_value": self.found_pet.age},
            {"attr": "sex", "label": "Sex", "lost_pet_value": self.lost_pet.sex, "found_pet_value": self.found_pet.sex},
            {"attr": "breed", "label": "Breed", "lost_pet_value": self.lost_pet.breed, "found_pet_value": self.found_pet.breed},
            {"attr": "color", "label": "Color", "lost_pet_value": self.lost_pet.color, "found_pet_value": self.found_pet.color},
            {"attr": "size", "label": "Size", "lost_pet_value": self.lost_pet.size, "found_pet_value": self.found_pet.size},
            {"attr": "tag_info", "label": "Tag and Collar Information", "lost_pet_value": self.lost_pet.tag_info, "found_pet_value": self.found_pet.tag_info},
            {"attr": "description", "label": "Description", "lost_pet_value": self.lost_pet.description, "found_pet_value": self.found_pet.description},
            {"attr": "contact_name", "label": "Alternate Contact Name", "lost_pet_value": self.lost_pet.contact_name, "found_pet_value": self.found_pet.contact_name},
            {"attr": "contact_number", "label": "Alternate Contact Number", "lost_pet_value": self.lost_pet.contact_number, "found_pet_value": self.found_pet.contact_number},
            {"attr": "contact_email", "label": "Alternate Contact Email Address", "lost_pet_value": self.lost_pet.contact_email, "found_pet_value": self.found_pet.contact_email},
            {"attr": "contact_link", "label": "Alternate Link to Pet", "lost_pet_value": self.lost_pet.contact_link, "found_pet_value": self.found_pet.contact_link},
        ]


    def to_JSON(self):
        return json.dumps(self.to_DICT())

    def is_successful(self):
        try:
            if self.petmatchcheck and self.petmatchcheck.is_successful:
                return True
        except:
            pass
        return False

    #Determine if a PetMatch exists between pr1 and pr2, and if so, return it. Otherwise, return None.
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
    def filter(params, page=1, limit=25):
        for key in params:
            if type(params[key]) == list:
                params[key] = params[key][0]
        params = {k:v for k, v in params.iteritems() if (v != "All" and k != "page")}
        petmatches = PetMatch.objects.filter(**params).order_by("id").reverse()
        count = len(petmatches)
        petmatches = get_objects_by_page(petmatches, page, limit)
        return {"petmatches": petmatches, "count":count}

    def is_being_checked(self):
        try:
            if self.petmatchcheck:
                return True
        except:
            return False

    def pack_PetReport_fields(self):
        return self.lost_pet.pack_PetReport_fields(other_pet=self.found_pet)

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

    def has_reached_threshold(self):
        from django.contrib.auth.models import User
        lost_pet_contact = self.lost_pet.proposed_by
        found_pet_contact = self.found_pet.proposed_by
        petmatch_owner = self.proposed_by

        if self.up_votes.count() > (User.objects.filter(is_active=True).count()/VERIFICATION_DEFAULT_THRESHOLD):
            print_info_msg("PetMatch %s has reached threshold!")
            return True
        else:
            return False


    def __unicode__ (self):
        return '{ID{%s} lost:%s, found:%s, proposed_by:%s}' % (self.id, self.lost_pet, self.found_pet, self.proposed_by)

#Create a pre-delete signal function to delete the corresponding PetMatchCheck object for the underlying PetMatch object.
@receiver (pre_delete, sender=PetMatch)
def delete_PetMatch(sender, instance=None, **kwargs):
    if instance.is_being_checked() == True:
        instance.petmatchcheck.delete()
        print_info_msg("PetMatchCheck %s has been deleted because %s has now been deleted." % (instance.petmatchcheck, instance))
