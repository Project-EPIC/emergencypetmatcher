from django.contrib import admin
from home.models import *

class PetReportAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {
            'fields': ('pet_type', 'status', 'date_lost_or_found','proposed_by','sex','size','location','pet_name','age','color','breed','description','workers')
        })
    ]
    
    list_display = ('id','pet_type', 'status', 'date_lost_or_found','proposed_by','sex','size','location','pet_name','age','color','breed') 

class PetMatchAdmin(admin.ModelAdmin):   
    list_display = ('id','lost_pet','found_pet','proposed_by','proposed_date','score','closed_by','closed_date')

class UserProfileInline(admin.StackedInline):
	model = UserProfile

class UserAdmin(admin.ModelAdmin):   
	inlines = [
		UserProfileInline,
	]
	list_display = ('id','username','first_name','last_name','email','is_staff','is_superuser','is_active')

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('id','user','reputation')	

admin.site.register(PetReport,PetReportAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(PetMatch,PetMatchAdmin)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
