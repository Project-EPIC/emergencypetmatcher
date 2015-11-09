from django.shortcuts import render_to_response, redirect, get_object_or_404
from reporting.models import PetReport
from verifying.models import PetMatchCheck
from django.contrib import messages
from home.constants import URL_HOME
import json, pdb

def allow_only_checkers(view_func):
  def _wrapped_view_func(request, *args, **kwargs):
    petmatchcheck = get_object_or_404(PetMatchCheck, pk=kwargs.get("petmatchcheck_id"))
    checkers = []
    checkers.append(petmatchcheck.petmatch.lost_pet.proposed_by)
    checkers.append(petmatchcheck.petmatch.found_pet.proposed_by)
    checkers.append(petmatchcheck.petmatch.proposed_by)
    profile = request.user.userprofile

    if profile not in checkers:
      messages.error(request, "Sorry, you cannot verify this pet match.")
      return redirect(URL_HOME)
    else:
      return view_func(request, *args, **kwargs)
  return _wrapped_view_func
