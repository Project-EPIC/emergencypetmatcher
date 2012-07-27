from django.contrib import admin
from home.models import *

class PetReportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ('pet_type', 'status', 'date_lost_or_found','proposed_by','sex','size','location','pet_name','age','color','breed','description','workers')
        })
    ]
    
    list_display = ('pet_type','proposed_by') 
admin.site.register(PetReport,PetReportAdmin)
admin.site.register(UserProfile)
admin.site.register(PetMatch)
