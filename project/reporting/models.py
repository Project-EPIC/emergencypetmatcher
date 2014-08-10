from django.db import models
from django.forms.models import model_to_dict
from social.models import UserProfile
from django.forms import ModelForm, Textarea
from django import forms
from django.core.files.images import ImageFile
from constants import *
from pprint import pprint
from utilities.utils import *
import simplejson, datetime

class PetReport(models.Model):
    '''Required Fields'''
    #Type of Pet
    pet_type = models.CharField(max_length=PETREPORT_PET_TYPE_LENGTH, choices = PET_TYPE_CHOICES, null=False, default=None)
    #Status of Pet (Lost/Found)
    status = models.CharField(max_length = PETREPORT_STATUS_LENGTH, choices = STATUS_CHOICES, null=False, default=None)
    #Date Lost/Found
    date_lost_or_found = models.DateField(null=False)
    #The UserProfile who is submitting this PetReport (ForeignKey: Many-to-one relationship with User)
    proposed_by = models.ForeignKey("social.UserProfile", null=False, default=None, related_name='proposed_related')

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
    #Contact Link for cross-referencing pet report.
    contact_link = models.CharField(max_length=PETREPORT_CONTACT_LINK_LENGTH, null=True)
    #Img of Pet
    img_path = models.ImageField(upload_to=PETREPORT_IMG_PATH, null=True)
    #Thumbnail Img of Pet
    thumb_path = models.ImageField(upload_to=PETREPORT_THUMBNAIL_PATH, null=True)
    #Spayed or Neutered?
    spayed_or_neutered = models.CharField(max_length=PETREPORT_SPAYED_OR_NEUTERED_LENGTH, choices=SPAYED_OR_NEUTERED_CHOICES, null=True, default="Unknown")
    #Pet Name (if available)
    pet_name = models.CharField(max_length=PETREPORT_PET_NAME_LENGTH, null=True, default='Name unknown') 
    #Pet Age (if known/available)
    age = models.CharField(max_length=PETREPORT_AGE_LENGTH, null=True, choices=AGE_CHOICES,default="Age unknown")
    #Color(s) of Pet
    color = models.CharField(max_length=PETREPORT_COLOR_LENGTH, null=True,default='Color(s) unknown')
    #Breed of Pet
    breed = models.CharField(max_length=PETREPORT_BREED_LENGTH, null=True,default='Breed unknown')
    #Description of Pet
    description   = models.CharField(max_length=PETREPORT_DESCRIPTION_LENGTH, null=True, default="")
    #The UserProfiles who are working on this PetReport (Many-to-Many relationship with User)
    workers = models.ManyToManyField("social.UserProfile", null=True, related_name='workers_related')
    #The UserProfiles who have bookmarked this PetReport
    bookmarked_by = models.ManyToManyField("social.UserProfile", null=True, related_name='bookmarks_related')
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

    def is_crossposted(self):
        if self.contact_email and email_is_valid(self.contact_email):
            return True
        return False

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
                img = img.rotate(rotation)
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

    @staticmethod
    def get_PetReports_by_page(filtered_petreports, page):
        if (page != None and page > 0):
            page = int(page)
            filtered_petreports = filtered_petreports [((page-1) * NUM_PETREPORTS_HOMEPAGE):((page-1) * NUM_PETREPORTS_HOMEPAGE + NUM_PETREPORTS_HOMEPAGE)]

        #Just return the list of PetReports.
        return filtered_petreports 

    @staticmethod
    def get_bookmarks_by_page(filtered_bookmarks, page):
        if (page != None and page > 0):
            page = int(page)
            filtered_bookmarks = filtered_bookmarks [((page-1) * NUM_BOOKMARKS_HOMEPAGE):((page-1) * NUM_BOOKMARKS_HOMEPAGE + NUM_BOOKMARKS_HOMEPAGE)]

        #Just return the list of bookmarks.
        return filtered_bookmarks   


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


    @staticmethod
    def get_field_label(field_name):
        if field_name == "status":
            return "Pet Status"
        elif field_name == "pet_type":
            return "Pet Type"
        elif field_name == "date_lost_or_found":
            return "Date Lost/Found"
        elif field_name == "proposed_by_username":
            return "Contact"
        elif field_name == "proposed_by":
            return "Contact ID"
        elif field_name == "pet_name":
            return "Pet Name"
        elif field_name == "location":
            return "Location"
        elif field_name == "microchip_id":
            return "Microchipped"
        elif field_name == "spayed_or_neutered":
            return "Spayed/Neutered"
        elif field_name == "age":
            return "Age"
        elif field_name == "sex":
            return "Sex"
        elif field_name == "breed":
            return "Breed"
        elif field_name == "color":
            return "Coat Color(s)"
        elif field_name == "size":
            return "Size"
        elif field_name == "tag_info":
            return "Tag and Collar Information"
        elif field_name == "description":
            return "Description"
        elif field_name == "contact_name":
            return "Contact Name"
        elif field_name == "contact_number":
            return "Contact Phone Number"
        elif field_name == "contact_link":
            return "Contact Link"
        elif field_name == "contact_email":
            return "Contact Email"
        else:
            return None

    def to_array(self):
        result = []
        result.append({"ID": self.id })
        result.append({"Pet Name": self.pet_name })
        result.append({"Pet Type": self.pet_type })
        result.append({"Lost/Found": self.status })
        result.append({"Contact": self.proposed_by.user.username })
        result.append({"Date Lost/Found": self.date_lost_or_found.strftime("%B %d, %Y") })
        result.append({"Location": self.location })
        result.append({"Microchipped": "Yes" if (self.microchip_id != "") else "No" })
        result.append({"Spayed/Neutered": self.spayed_or_neutered })
        result.append({"Age": self.age })
        result.append({"Sex": self.sex })
        result.append({"Breed": self.breed })
        result.append({"Color": self.color })
        result.append({"Size": self.size })
        result.append({"Tag and Collar Information": self.tag_info })
        result.append({"Description": self.description })
        result.append({"Contact Name": self.contact_name })
        result.append({"Contact Phone Number": self.contact_number })
        result.append({"Contact Email Address": self.contact_email })
        result.append({"Alternative Link to Pet": self.contact_link })
        return result

    def pack_PetReport_fields(self, other_pet=None):
        fields = []
        pet = self.to_array()
        if isinstance(other_pet, PetReport):
            other_pet = other_pet.to_array()

        for i in range(len(pet)):
            field = []
            label = pet[i].keys()[0]
            field.append(label)
            field.append(pet[i][label])

            if other_pet != None:
                field.append(other_pet[i][label])
            fields.append(field)
        return fields       

    def toDICT(self):
        #A customized version of django model function "model_to_dict"
        #to convert a PetReport model object to a dictionary object
        modeldict = model_to_dict(self)

        #Iterate through all fields in the model_dict
        for field in modeldict:
            value = modeldict[field]
            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                # print_debug_msg(value)
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
        pprint(modeldict)     
        return modeldict


    def toJSON(self):
        #Convert a PetReport model object to a json object
        json = simplejson.dumps(self.toDICT())
        #print_info_msg("toJSON: " + str(json))
        return json


#The PetReport ModelForm
class PetReportForm (ModelForm):

    '''Required Fields'''
    pet_type = forms.ChoiceField(label = 'Pet Type', choices = PET_TYPE_CHOICES, required = True)  
    status = forms.ChoiceField(label = "Pet Status", help_text="(Lost/Found)", choices = STATUS_CHOICES, required = True)
    date_lost_or_found = forms.DateField(label = "Date Lost/Found", widget = forms.DateInput, required = True)

    '''Non-Required Fields'''
    pet_name = forms.CharField(label = "Pet Name", max_length=PETREPORT_PET_NAME_LENGTH, required = False) 
    age = forms.ChoiceField(label = "Age", choices=AGE_CHOICES,required = False)
    breed = forms.CharField(label = "Breed", max_length = PETREPORT_BREED_LENGTH, required = False)
    color = forms.CharField(label = "Coat Color(s)", max_length = PETREPORT_COLOR_LENGTH, required = False)    
    sex = forms.ChoiceField(label = "Sex", choices = SEX_CHOICES, required = False)
    size = forms.ChoiceField(label = "Size of Pet", choices = SIZE_CHOICES, required = False)
    location = forms.CharField(label = "Location", help_text="(Location where pet was lost/found)", max_length = PETREPORT_LOCATION_LENGTH , required = False)
    geo_location_lat = forms.DecimalField(label = "Geo Location Lat", help_text="(Latitude coordinate)", max_digits=8, decimal_places=5, widget=forms.TextInput(attrs={'size':'10'}), initial=None, required=False)
    geo_location_long = forms.DecimalField(label = "Geo Location Long", help_text="(Longitude coordinate)", max_digits=8, decimal_places=5, widget=forms.TextInput(attrs={'size':'10'}),  initial=None, required=False)
    microchip_id = forms.CharField(label = "Microchip ID", max_length = PETREPORT_MICROCHIP_ID_LENGTH, required=False)
    tag_info = forms.CharField(label = "Tag and Collar Information", help_text="(if available)", max_length = PETREPORT_TAG_INFO_LENGTH, required=False, widget=Textarea)
    contact_name = forms.CharField(label = "Contact Name", max_length=PETREPORT_CONTACT_NAME_LENGTH, required=False)
    contact_number = forms.CharField(label = "Contact Phone Number", max_length=PETREPORT_CONTACT_NUMBER_LENGTH, required=False)
    contact_email = forms.CharField(label = "Contact Email Address", max_length=PETREPORT_CONTACT_EMAIL_LENGTH, required=False)
    contact_link = forms.CharField(label = "Contact Alternative link to Pet Posting", max_length=PETREPORT_CONTACT_LINK_LENGTH, required=False)
    img_path = forms.ImageField(label = "Upload an Image", help_text="(*.jpg, *.png, *.bmp), 3MB maximum", widget = forms.ClearableFileInput, required = False)
    spayed_or_neutered = forms.ChoiceField(label="Spayed/Neutered", choices=SPAYED_OR_NEUTERED_CHOICES, required=False)
    description  = forms.CharField(label = "Pet Description", help_text="(Please describe the pet as accurately as possible)", max_length = PETREPORT_DESCRIPTION_LENGTH, widget = forms.Textarea, required = False)

    class Meta:
        model = PetReport
        #exclude = ('revision_number', 'workers', 'proposed_by','bookmarked_by','closed', 'thumb_path')
        fields = ("status", "date_lost_or_found", "pet_type", "pet_name",  "breed", "age", "color", "sex", "spayed_or_neutered", "size", "img_path", "description", "location", "geo_location_lat", "geo_location_long", "microchip_id", "tag_info", "contact_name", "contact_number", "contact_email", "contact_link")

