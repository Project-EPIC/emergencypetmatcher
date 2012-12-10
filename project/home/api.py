# home/api.py
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.exceptions import *
from home.models import UserProfile, PetReport
from django.db import IntegrityError
from datetime import datetime
from django.core.exceptions import ValidationError
from utils import *
from logging import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get', 'post', 'put']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        
class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True) 
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'userprofile'        

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data, format)


class PetReportResource(MultipartResource, ModelResource):
    proposed_by = fields.ForeignKey(UserProfileResource, 'proposed_by', full=True)

    class Meta:
        queryset = PetReport.objects.all()
        resource_name = 'petreport'
        # include_resource_uri = False
        allowed_methods = ['get', 'post']
        authentication = BasicAuthentication()
        authorization = Authorization()
        always_return_data=True

    def obj_create(self, bundle, request=None, **kwargs):
        
        try: 
            print bundle
            form = PetReportForm(bundle.data)

            if form.is_valid() == True:
                pr = form.save(commit=False)
                #Create (but do not save) the Pet Report Object associated with this form data.
                pr.proposed_by = request.user.get_profile()
                print "[INFO]: Pet Report Image Path: %s" % pr.img_path
                #If there was no image attached, let's take care of defaults.
                if pr.img_path == None:
                    if pr.pet_type == PETREPORT_PET_TYPE_DOG:
                        pr.img_path.name = "images/defaults/dog_silhouette.jpg"
                    elif pr.pet_type == PETREPORT_PET_TYPE_CAT:
                        pr.img_path.name = "images/defaults/cat_silhouette.jpg"
                    elif pr.pet_type == PETREPORT_PET_TYPE_BIRD:
                        pr.img_path.name = "images/defaults/bird_silhouette.jpg"                    
                    elif pr.pet_type == PETREPORT_PET_TYPE_HORSE:
                        pr.img_path.name = "images/defaults/horse_silhouette.jpg"
                    elif pr.pet_type == PETREPORT_PET_TYPE_RABBIT:
                        pr.img_path.name = "images/defaults/rabbit_silhouette.jpg"
                    elif pr.pet_type == PETREPORT_PET_TYPE_SNAKE:
                        pr.img_path.name = "images/defaults/snake_silhouette.jpg"                                       
                    elif pr.pet_type == PETREPORT_PET_TYPE_TURTLE:
                        pr.img_path.name = "images/defaults/turtle_silhouette.jpg"
                    else:
                        pr.img_path.name = "images/defaults/other_silhouette.jpg"
        
                #Now save the Pet Report.        
                pr.save() 
                if pr.status == 'Lost':
                    bundle.data ['message'] = 'Thank you for your submission! Your contribution will go a long way towards helping people find your lost pet.'
                else:
                    bundle.data ['message'] = 'Thank you for your submission! Your contribution will go a long way towards helping others match lost and found pets.'

                #Log the PetReport submission for this UserProfile
                log_activity(ACTIVITY_PETREPORT_SUBMITTED, request.user.get_profile(), petreport=pr)
                print "[SUCCESS]: Pet Report submitted successfully" 
                bundle.obj = pr

        except Exception as e:
            raise BadRequest(e)

        return bundle


class PetReportResource2(MultipartResource, ModelResource):
    proposed_by = fields.ForeignKey(UserProfileResource, 'proposed_by', full=True)
    
    class Meta:
        queryset = PetReport.objects.all()
        resource_name = 'petreport2'
        # include_resource_uri = False
        allowed_methods = ['get', 'post']
        authentication = BasicAuthentication()
        authorization = Authorization()
        always_return_data=True
        #fields = ('pet_type', 'status', 'date_lost_or_found','sex','size','location','proposed_by','img_path')

    def obj_create(self, bundle, request=None, **kwargs):
        try: 
            # Read sent input data from bundle object
            '''Required Fields'''
            pet_type = bundle.data['pet_type']
            status = bundle.data['status']
            date_lost_or_found = datetime.strptime(bundle.data['date_lost_or_found'], '%m/%d/%Y')
            sex = bundle.data['sex']
            size = bundle.data['size']
            location = bundle.data['location']
            proposed_by = request.user.get_profile()
            '''Non-Required Fields'''
            img_path = ""
            pet_name = ""
            age= ""
            color = ""
            breed = ""
            description = ""
            if 'img_path' in bundle.data: img_path = bundle.data['img_path']
            if img_path == "":
                if pet_type == "Dog":
                    img_path.name = "images/defaults/dog_silhouette.jpg"
                elif pet_type == "Cat":
                    img_path = "images/defaults/cat_silhouette.jpg"
                elif pet_type == "Horse":
                    img_path.name = "images/defaults/horse_silhouette.jpg"
                elif pet_type == "Rabbit":
                    img_path.name = "images/defaults/rabbit_silhouette.jpg"
                elif pet_type == "Snake":
                    img_path.name = "images/defaults/snake_silhouette.jpg"                                       
                elif pet_type == "Turtle":
                    img_path.name = "images/defaults/turtle_silhouette.jpg"
                else:
                    img_path.name = "images/defaults/other_silhouette.jpg"
            # if img_path is not found
            if 'pet_name' in bundle.data: pet_name = bundle.data['pet_name']
            if 'age' in bundle.data: age = bundle.data['age']
            if 'color' in bundle.data: color = bundle.data['color']
            if 'breed' in bundle.data: breed = bundle.data['breed']
            if 'description' in bundle.data: description = bundle.data['description']
            # Create a PetReport object
            try:
                pr = PetReport(pet_type=pet_type, status=status, date_lost_or_found=date_lost_or_found, 
                    sex=sex, size=size, location=location, proposed_by=proposed_by, 
                    img_path=img_path, pet_name=pet_name, age=age, color=color, breed=breed, description=description)
                bundle.obj = pr
                bundle.obj.save()
                log_activity(ACTIVITY_PETREPORT_SUBMITTED, proposed_by, petreport=pr)
            except IntegrityError:
                raise BadRequest('That petreport already exists\n')
        except Exception:
            raise BadRequest('Please include all the required fields to submit a petreport\n')
        return bundle

  

 
