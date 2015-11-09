from django.shortcuts import render_to_response, redirect, get_object_or_404
from reporting.models import PetReport
from matching.models import PetMatch
from django.contrib import messages
from home.constants import URL_HOME
from matching.constants import URL_MATCHING
import json, pdb

def disallow_closed_petreports(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        for key in kwargs.keys():
            if get_object_or_404(PetReport, pk=kwargs[key]).closed == True:
                messages.error(request, "This pet has already been closed.")
                return redirect(URL_HOME)
            else:
                return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def disallow_incompatible_petreports(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        target_petreport = get_object_or_404(PetReport, pk=kwargs["target_id"])
        candidate_petreport = get_object_or_404(PetReport, pk=kwargs["candidate_id"])
        if target_petreport.status == candidate_petreport.status:
            messages.error(request, "Proposed pet reports cannot both be '%s'!" % (target_petreport.status))
            return redirect(URL_MATCHING + str(target_petreport.id))
        if target_petreport.pet_type != candidate_petreport.pet_type:
            messages.error(request, "Proposed pet reports cannot have different pet types!")
            return redirect(URL_MATCHING + str(target_petreport.id))
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def allow_only_before_closing(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        pm = get_object_or_404(PetMatch, pk=kwargs["petmatch_id"])
        if pm.is_being_checked():
            messages.error(request, "This PetMatch is currently being checked. All voting is closed.")
        elif pm.lost_pet.closed or pm.found_pet.closed:
            messages.error(request, "This PetMatch is closed because one of the pet reports is closed.")
        else:
            return view_func(request, *args, **kwargs)
        return redirect(URL_HOME)
    return _wrapped_view_func
