from django.db import models
from django.forms.models import model_to_dict
from socializing.models import UserProfile
from django.forms import ModelForm, Textarea
from django import forms
from django.core.files.images import ImageFile
from constants import *
from pprint import pprint
from utilities.utils import *
import json, datetime

class PetReport(models.Model):
    '''Required Fields'''
    #Type of Pet
    pet_type = models.CharField(max_length=PETREPORT_PET_TYPE_LENGTH, choices = PET_TYPE_CHOICES, null=False, default=None)
    #Status of Pet (Lost/Found)
    status = models.CharField(max_length = PETREPORT_STATUS_LENGTH, choices = STATUS_CHOICES, null=False, default=None)
    #Date Lost/Found
    date_lost_or_found = models.DateField(null=False)
    #The UserProfile who is submitting this PetReport (ForeignKey: Many-to-one relationship with User)
    proposed_by = models.ForeignKey("socializing.UserProfile", null=False, default=None, related_name='proposed_related')

    '''Non-Required Fields'''
    #Sex of the Pet
    sex = models.CharField(max_length=PETREPORT_SEX_LENGTH, choices=SEX_CHOICES, null=True)
    #Size of the Pet, in ranges
    size = models.CharField(max_length=PETREPORT_SIZE_LENGTH, choices=SIZE_CHOICES, null=True)
    #Location where found
    location = models.CharField(max_length=PETREPORT_LOCATION_LENGTH, null=True)
    #Lat/Long Geo-coordinates of Location
    geo_location_lat = models.FloatField(null=True, default=0.0)
    geo_location_long = models.FloatField(null=True, default=0.0)
    #Microchip ID of Pet
    microchip_id = models.CharField(max_length=PETREPORT_MICROCHIP_ID_LENGTH, null=True)
    #Pet Tag Information (if available)
    tag_info = models.CharField(max_length=PETREPORT_TAG_INFO_LENGTH, null=True, default="")
    #Contact Name of Person who is sheltering/reporting lost/found Pet (if different than proposed_by UserProfile)
    contact_name = models.CharField(max_length=PETREPORT_CONTACT_NAME_LENGTH, null=True, default="None")
    #Contact Phone Number of Person who is sheltering/reporting lost/found Pet (if different than proposed_by UserProfile)
    contact_number = models.CharField(max_length=PETREPORT_CONTACT_NUMBER_LENGTH, null=True, default="None")
    #Contact Email Address of Person who is sheltering/reporting lost/found Pet (if different than proposed_by UserProfile)
    contact_email = models.CharField(max_length=PETREPORT_CONTACT_EMAIL_LENGTH, null=True, default="None")        
    #Contact Link for cross-referencing pet report.
    contact_link = models.CharField(max_length=PETREPORT_CONTACT_LINK_LENGTH, null=True, default="None")
    #Img of Pet
    img_path = models.ImageField(upload_to=PETREPORT_IMG_PATH, null=True)
    #Thumbnail Img of Pet
    thumb_path = models.ImageField(upload_to=PETREPORT_THUMBNAIL_PATH, null=True)
    #Spayed or Neutered?
    spayed_or_neutered = models.CharField(max_length=PETREPORT_SPAYED_OR_NEUTERED_LENGTH, choices=SPAYED_OR_NEUTERED_CHOICES, null=True, default="Not Known")
    #Pet Name (if available)
    pet_name = models.CharField(max_length=PETREPORT_PET_NAME_LENGTH, null=True, default='unknown') 
    #Pet Age (if known/available)
    age = models.CharField(max_length=PETREPORT_AGE_LENGTH, null=True, choices=AGE_CHOICES,default="Age unknown")
    #Color(s) of Pet
    color = models.CharField(max_length=PETREPORT_COLOR_LENGTH, null=True,default='Color(s) unknown')
    #Breed of Pet
    breed = models.CharField(max_length=PETREPORT_BREED_LENGTH, null=True,default='Breed unknown')
    #Description of Pet
    description   = models.CharField(max_length=PETREPORT_DESCRIPTION_LENGTH, null=True, default="")
    #The UserProfiles who are working on this PetReport (Many-to-Many relationship with User)
    workers = models.ManyToManyField("socializing.UserProfile", related_name='workers_related')
    #The UserProfiles who have bookmarked this PetReport
    bookmarked_by = models.ManyToManyField("socializing.UserProfile", related_name='bookmarks_related')
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

    def to_DICT(self, ):
        return {    
        "id"                    : self.id,
        "pet_type"              : self.pet_type,
        "status"                : self.status,
        "date_lost_or_found"    : self.date_lost_or_found.strftime("%B %d, %Y"),
        "proposed_by_username"  : self.proposed_by.user.username,
        "proposed_by_id"        : self.proposed_by.id,
        "sex"                   : self.sex,
        "size"                  : self.size,
        "location"              : self.location,
        "geo_lat"               : str(self.geo_location_lat),
        "geo_long"              : str(self.geo_location_long),
        "microchip_id"          : "Yes" if (self.microchip_id != "") else "No" ,
        "tag_info"              : self.tag_info,
        "contact_name"          : self.contact_name,
        "contact_number"        : self.contact_number,
        "contact_email"         : self.contact_email,
        "contact_link"          : self.contact_link,
        "img_path"              : self.img_path.name,
        "thumb_path"            : self.thumb_path.name,
        "spayed_or_neutered"    : self.spayed_or_neutered,
        "pet_name"              : self.pet_name,
        "age"                   : self.age,
        "color"                 : self.color,
        "breed"                 : self.breed,
        "description"           : self.description,
        "closed"                : self.closed 
        }

    def to_JSON(self):
        return json.dumps(self.to_DICT())                  

    #Determine if the input UserProfile (user) has bookmarked this PetReport already
    def UserProfile_has_bookmarked(self, user_profile):
        assert isinstance(user_profile, UserProfile)
        try:
            user = self.bookmarked_by.get(pk = user_profile.id)
            return True
        except UserProfile.DoesNotExist:
            return False

    def UserProfile_is_owner(self, userprofile):
        return userprofile.id == self.proposed_by.id

    def is_crossposted(self):
        if self.contact_email and email_is_valid(self.contact_email):
            return True
        return False

    def update_fields(self, pr, request=None):
        self.pet_type           = pr.pet_type
        self.status             = pr.status
        self.date_lost_or_found = pr.date_lost_or_found
        self.sex                = pr.sex
        self.spayed_or_neutered = pr.spayed_or_neutered
        self.pet_name           = pr.pet_name
        self.size               = pr.size
        self.age                = pr.age
        self.color              = pr.color
        self.breed              = pr.breed        
        self.location           = pr.location
        self.geo_location_lat   = pr.geo_location_lat
        self.geo_location_long  = pr.geo_location_long
        self.microchip_id       = pr.microchip_id
        self.tag_info           = pr.tag_info
        self.description        = pr.description
        self.contact_name       = pr.contact_name
        self.contact_number     = pr.contact_number
        self.contact_email      = pr.contact_email
        self.contact_link       = pr.contact_link

        #Only change if incoming PetReport's image is different.
        if pr.img_path.name and self.img_path != pr.img_path:
            self.set_images(pr.img_path, save=True, rotation=request.get("img_rotation"))
        else:
            self.save()

    #Make and save images from img_path and thumb_path AND save the PetReport.
    # pr.set_images(pr.img_path, save=True, rotation=img_rotation)


    #This function returns True if any marked-successful PetCheck object has been set involving this PetReport, False otherwise.
    def has_been_successfully_matched(self):
        for pm in self.get_all_PetMatches():
            if pm.is_being_checked() == True:
                if pm.petcheck.is_successful == True:
                    return True
        return False

    def get_all_PetMatches(self):
        if self.status == "Lost":
            return list(models.get_model("matching", "PetMatch").objects.filter(lost_pet=self))
        elif self.status == "Found":
            return list(models.get_model("matching", "PetMatch").objects.filter(found_pet=self))
        else:
            return None      
    
    #set_img_path(): Sets the image path and thumb path for this PetReport. Save is optional.
    def set_images(self, img_path, save=True, rotation=None):
        #Deal with the 'None' case.
        if img_path == None:
            if self.pet_type == PETREPORT_PET_TYPE_DOG:
                self.img_path = PETREPORT_UPLOADS_DEFAULT_DOG_IMAGE
                self.thumb_path = PETREPORT_THUMBNAILS_DEFAULT_DOG_IMAGE

            elif self.pet_type == PETREPORT_PET_TYPE_CAT:
                self.img_path = PETREPORT_UPLOADS_DEFAULT_CAT_IMAGE
                self.thumb_path = PETREPORT_THUMBNAILS_DEFAULT_CAT_IMAGE

            elif self.pet_type == PETREPORT_PET_TYPE_BIRD:
                self.img_path = PETREPORT_UPLOADS_DEFAULT_BIRD_IMAGE                    
                self.thumb_path = PETREPORT_THUMBNAILS_DEFAULT_BIRD_IMAGE

            elif self.pet_type == PETREPORT_PET_TYPE_HORSE:
                self.img_path = PETREPORT_UPLOADS_DEFAULT_HORSE_IMAGE
                self.thumb_path = PETREPORT_THUMBNAILS_DEFAULT_HORSE_IMAGE

            elif self.pet_type == PETREPORT_PET_TYPE_RABBIT:
                self.img_path = PETREPORT_UPLOADS_DEFAULT_RABBIT_IMAGE
                self.thumb_path = PETREPORT_THUMBNAILS_DEFAULT_RABBIT_IMAGE

            elif self.pet_type == PETREPORT_PET_TYPE_SNAKE:
                self.img_path = PETREPORT_UPLOADS_DEFAULT_SNAKE_IMAGE
                self.thumb_path = PETREPORT_THUMBNAILS_DEFAULT_SNAKE_IMAGE

            elif self.pet_type == PETREPORT_PET_TYPE_TURTLE:
                self.img_path = PETREPORT_UPLOADS_DEFAULT_TURTLE_IMAGE
                self.thumb_path = PETREPORT_THUMBNAILS_DEFAULT_TURTLE_IMAGE
                
            else:
                self.img_path = PETREPORT_UPLOADS_DEFAULT_OTHER_IMAGE
                self.thumb_path = PETREPORT_THUMBNAILS_DEFAULT_OTHER_IMAGE

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
                if rotation != None:
                    img = img.rotate(-int(rotation))
                
                self.img_path = PETREPORT_IMG_PATH + unique_img_name
                self.thumb_path = PETREPORT_THUMBNAIL_PATH + unique_img_name
                img.save(PETREPORT_UPLOADS_DIRECTORY + unique_img_name, "JPEG", quality=75)
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

    def get_display_fields(self):
        return [
            {"attr": "pet_name", "label": "Pet Name", "value": self.pet_name},
            {"attr": "pet_type", "label": "Pet Type", "value": self.pet_type},
            {"attr": "status", "label": "Lost/Found", "value": self.status},
            {"attr": "date_lost_or_found", "label": "Date Lost/Found", "value": self.date_lost_or_found.strftime("%B %d, %Y")},
            {"attr": "proposed_by_username", "label": "Contact", "value": self.proposed_by.user.username},
            {"attr": "location", "label": "Location", "value": self.location},
            {"attr": "microchip_id", "label": "Microchipped?", "value": "Yes" if (self.microchip_id != "") else "No"},
            {"attr": "spayed_or_neutered", "label": "Spayed/Neutered", "value": self.spayed_or_neutered},
            {"attr": "age", "label": "Age", "value": self.age},
            {"attr": "sex", "label": "Sex", "value": self.sex},
            {"attr": "breed", "label": "Breed", "value": self.breed},
            {"attr": "color", "label": "Color", "value": self.color},
            {"attr": "size", "label": "Size", "value": self.size},
            {"attr": "tag_info", "label": "Tag and Collar Information", "value": self.tag_info},
            {"attr": "description", "label": "Description", "value": self.description},
            {"attr": "contact_name", "label": "Alternate Contact Name", "value": self.contact_name},
            {"attr": "contact_number", "label": "Alternate Contact Number", "value": self.contact_number},
            {"attr": "contact_email", "label": "Alternate Contact Email Address", "value": self.contact_email},
            {"attr": "contact_link", "label": "Alternate Link to Pet", "value": self.contact_link},
        ]


    @staticmethod
    def filter(options):
        pet_reports = PetReport.objects
        if options.get("status"):
            pet_reports = pet_reports.filter(status=options["status"])
        if options.get("pet_type"):
            pet_reports = pet_reports.filter(pet_type=options["pet_type"])
        if options.get("pet_name"):
            pet_reports = pet_reports.filter(pet_name=options["pet_name"])
        return pet_reports

    #Return a count of candidate PetReports that could potentially be matches for this PetReport.
    def get_candidate_PetReports(self):
        pets = PetReport.objects.exclude(status=self.status).filter(pet_type=self.pet_type, closed=False)
        if (self.contact_email): #If this pet has an alternate contact, then all pets are fair game to match.
            return pets

        #otherwise, exclude pets that have the same proposer and no alternate contacts.
        return pets.exclude(proposed_by=self.proposed_by, contact_email=None)

    #this function compares attributes of both pets and returns the number of matching attributes.
    def compare(self, petreport):
        assert isinstance (petreport, PetReport)
        rank = 0

        #Lat & Long
        if round(self.geo_location_lat, 2) == round(petreport.geo_location_lat, 2):
            if round(self.geo_location_long, 2) == round(petreport.geo_location_long, 2):
                rank += 2
        #Location
        if self.location.lower() == petreport.location.lower():
            rank += 2
        #Sex
        if self.sex == petreport.sex:
            rank += 1
        #Size
        if self.size == petreport.size:
            rank += 1
        #Spayed/Neutered
        if self.spayed_or_neutered == petreport.spayed_or_neutered:
            rank += 1
        #Pet Name
        if self.pet_name.lower() == petreport.pet_name.lower():
            rank += 1
        #Breed
        if self.breed.lower() == petreport.breed.lower():
            rank += 1
        #Age
        if self.age == petreport.age:
            rank += 1
        #Color
        if self.color.lower() == petreport.color.lower():
            rank += 1

        return rank  

    #This method returns a ranked list of all PetReports found in the input specified list. This ranking is based on the PetReport compare() method.
    def get_ranked_candidate_PetReports(self, candidates, page=None):
        #Begin criteria ranking process: Sort/Rank based on how many similar PetReport features occur between target and candidate.
        results = []            
        for candidate in candidates:
            results.append((candidate, self.compare(candidate))) 

        #Perform sort w.r.t rankings.
        results = [x for (x,y) in sorted(results, reverse=True, key=lambda x: x[1])]
        return get_objects_by_page(results, page, limit=NUM_PETREPORTS_HOMEPAGE)

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

#The PetReport ModelForm
class PetReportForm (ModelForm):

    '''Required Fields'''
    pet_type            = forms.ChoiceField(label='Pet Type', choices = PET_TYPE_CHOICES, required = True, widget=forms.Select(attrs={"class":"form-control", "style":"width:100px"}))  
    status              = forms.ChoiceField(label="Pet Status", help_text="(Lost/Found)", choices = STATUS_CHOICES, required = True, widget=forms.Select(attrs={"class":"form-control","style":"width:100px"}))
    date_lost_or_found  = forms.DateField(label="Date Lost/Found", required = True,  widget = forms.DateInput(attrs={"class":"form-control", "style":"width:200px"}))

    '''Non-Required Fields'''
    pet_name            = forms.CharField(label="Pet Name", max_length=PETREPORT_PET_NAME_LENGTH, required = False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:150px", "placeholder":"If Available"})) 
    age                 = forms.ChoiceField(label="Age", choices=AGE_CHOICES,required = False, widget = forms.Select(attrs={"class":"form-control", "style":"width:100px"}))
    breed               = forms.CharField(label="Breed", max_length = PETREPORT_BREED_LENGTH, required = False, widget=forms.TextInput(attrs={"style":"width:200px; display:block;"}))
    color               = forms.CharField(label="Coat Color(s)", max_length = PETREPORT_COLOR_LENGTH, required = False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:200px", "placeholder":"Example: Brown, White"}))    
    sex                 = forms.ChoiceField(label="Sex", choices = SEX_CHOICES, required = False, widget = forms.Select(attrs={"class":"form-control", "style":"width:100px"}))
    size                = forms.ChoiceField(label="Size of Pet", choices = SIZE_CHOICES, required = False, widget=forms.Select(attrs={"class":"form-control", "style":"width:200px"}))
    location            = forms.CharField(label="Location", help_text="(Location where pet was lost/found)", max_length = PETREPORT_LOCATION_LENGTH , required=False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:500px; margin-bottom:10px;", "placeholder": "Write in general information, such as 'Boulder, CO'"}))
    geo_location_lat    = forms.FloatField(label="Geo Location Lat", help_text="(Latitude coordinate)", initial=None, required=False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:245px; margin-bottom:10px;", "placeholder": "Latitude (Lat)"}))
    geo_location_long   = forms.FloatField(label="Geo Location Long", help_text="(Longitude coordinate)", initial=None, required=False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:245px; margin-bottom:10px;", "placeholder": "Longitude (Long)"}))
    microchip_id        = forms.CharField(label="Microchip ID", max_length = PETREPORT_MICROCHIP_ID_LENGTH, required=False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:380px", "placeholder": "Pet Microchip ID"}))
    tag_info            = forms.CharField(label="Tag and Collar Information", max_length = PETREPORT_TAG_INFO_LENGTH, required=False, widget=Textarea(attrs={"class":"form-control", "placeholder":"(Please write tag collar information only if is available)", "style":"max-width:400px; max-height:300px;"}))
    contact_name        = forms.CharField(label="Contact Name", max_length=PETREPORT_CONTACT_NAME_LENGTH, required=False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:200px; margin-bottom:10px;"}))
    contact_number      = forms.CharField(label="Contact Phone Number", max_length=PETREPORT_CONTACT_NUMBER_LENGTH, required=False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:250px; margin-bottom:10px;"}))
    contact_email       = forms.CharField(label="Contact Email Address", max_length=PETREPORT_CONTACT_EMAIL_LENGTH, required=False, widget=forms.TextInput(attrs={"class":"form-control", "style":"width:200px; margin-bottom:10px;"}))
    contact_link        = forms.CharField(label="Contact Alternative link to Pet Posting", max_length=PETREPORT_CONTACT_LINK_LENGTH, required=False, widget=forms.TextInput(attrs={"class":"form-control", "style":"font-family:monospace; width:500px"}))
    img_path            = forms.ImageField(label="Upload an Image", help_text="(*.jpg, *.png, *.bmp), 3MB maximum", required = False, widget=forms.FileInput)
    spayed_or_neutered  = forms.ChoiceField(label="Spayed/Neutered", choices=SPAYED_OR_NEUTERED_CHOICES, required=False, widget=forms.Select(attrs={"class":"form-control", "style":"width:200px"}))
    description         = forms.CharField(label="Pet Description", max_length = PETREPORT_DESCRIPTION_LENGTH, required = False, widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "(Please describe the pet as accurately as possible)", "style":"max-width:400px; max-height:300px;"}))

    class Meta:
        model = PetReport
        #exclude = ('revision_number', 'workers', 'proposed_by','bookmarked_by','closed', 'thumb_path')
        fields = ("status", "date_lost_or_found", "pet_type", "pet_name",  "breed", "age", "color", "sex", "spayed_or_neutered", "size", "microchip_id", "img_path", "description", "location", "geo_location_lat", "geo_location_long", "tag_info", "contact_name", "contact_number", "contact_email", "contact_link")

