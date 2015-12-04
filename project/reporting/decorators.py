from django.shortcuts import render_to_response, redirect, get_object_or_404
from reporting.models import PetReport
from django.contrib import messages
from reporting.constants import URL_PRDP
import json, ipdb

def allow_only_proposer(view_func):
  def _wrapped_view_func(request, *args, **kwargs): 
    userprofile = request.user.userprofile
    petreport = get_object_or_404(PetReport, pk=kwargs.get("petreport_id"))
    if petreport.proposed_by != userprofile:
      messages.error(request, "Sorry, you are not this pet's reporter.")
      return redirect(URL_PRDP + str(petreport.id))            
    else:
      return view_func(request, *args, **kwargs)     
  return _wrapped_view_func

def allow_only_one_close(view_func):
  def _wrapped_view_func(request, *args, **kwargs): 
    petreport = get_object_or_404(PetReport, pk=kwargs.get("petreport_id"))
    if petreport.get_PetReunion() != None:
      messages.error(request, "This pet has already been closed.")
      return redirect(URL_PRDP + str(petreport.id))            
    else:
      return view_func(request, *args, **kwargs)     
  return _wrapped_view_func

def allow_only_before_close(view_func):
  def _wrapped_view_func(request, *args, **kwargs): 
    petreport = get_object_or_404(PetReport, pk=kwargs.get("petreport_id"))
    if petreport.get_PetReunion() != None:
      messages.error(request, "This pet report cannot be edited after closing.")
      return redirect(URL_PRDP + str(petreport.id))            
    else:
      return view_func(request, *args, **kwargs)     
  return _wrapped_view_func

