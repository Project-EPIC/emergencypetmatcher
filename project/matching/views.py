# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from django.db.models import Min
from social_auth import __version__ as version
from social_auth.utils import setting
from django.contrib.messages.api import get_messages
from social_auth.views import auth
from django.db import IntegrityError
from home.models import *
from django.http import Http404
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from random import choice, uniform
import re

@login_required
def matching(request, petreport_id):

	#Get Pet Report objects and organize them into a Paginator Object.
    target_prdp = PetReport.objects.get(pk = petreport_id)
    pet_reports = PetReport.objects.all().exclude(status = target_prdp.status)
    paginator = Paginator(pet_reports, 100)
    page = request.GET.get('page')
  
    try:
        pet_reports_list = paginator.page(page)
    except PageNotAnInteger:
        pet_reports_list = paginator.page(1)
    except EmptyPage:
        pet_reports_list = paginator.page(paginator.num_pages)

    return render_to_response ('matching/matching.html', {'target_prdp':target_prdp, 'pet_reports_list': pet_reports_list}, RequestContext(request))