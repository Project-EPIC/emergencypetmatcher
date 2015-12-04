from django.shortcuts import render_to_response, redirect, get_object_or_404
from socializing.models import UserProfile
from django.contrib import messages
from home.constants import URL_HOME
import json, ipdb

def allow_only_userprofile_owner(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.userprofile.id != int(kwargs.get("userprofile_id")):
            messages.error(request, "You cannot edit another user's profile.")
            return redirect(URL_HOME)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
