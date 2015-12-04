from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from socializing.models import UserProfile, UserProfileForm, EditUserProfile
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404, render_to_response, redirect
from home.models import Activity
from datetime import datetime
from constants import *
from socializing.decorators import *
from home.constants import *
from utilities.utils import *
from pprint import pprint
import ipdb

@login_required
def get(request, userprofile_id):
    #Be aware of what you show other authenticated users in contrast to the *same* authenticated user.
    request_profile = request.user.userprofile
    show_profile = get_object_or_404(UserProfile, pk=userprofile_id)
    context = {"show_profile": show_profile}

    if request_profile.id == show_profile.id:
        context["following_list"] = show_profile.following.all()
        context["followers_list"] = show_profile.followers.all()

    context["proposed_petreports"] = show_profile.proposed_related.all()
    context["proposed_petmatches"] = show_profile.proposed_by_related.all()
    return render_to_response(HTML_USERPROFILE, context, RequestContext(request))

def get_UserProfiles_JSON(request):
    if request.is_ajax() == True:
        filters = dict(request.GET)
        #Grab UserProfiles by Filter Options.
        results = UserProfile.filter(filters, page=request.GET["page"], limit=10)
        userprofiles = [{
            "ID"            : u.id,
            "username"      : u.user.username,
            "email"         : u.user.email,
            "first_name"    : u.user.first_name,
            "last_name"     : u.user.last_name,
        } for u in results["userprofiles"]]

        return JsonResponse({"userprofiles_list":userprofiles, "count":len(userprofiles), "total_count": results["count"]}, safe=False)
    else:
        raise Http404

@login_required
def follow(request):
    if request.method == "POST":
        userprofile = request.user.userprofile
        target_userprofile_id = request.POST["target_userprofile_id"]
        target_userprofile = get_object_or_404(UserProfile, pk=target_userprofile_id)

        if userprofile.id != target_userprofile.id:
            if target_userprofile in userprofile.following.all():
                messages.error(request, "You are already following " + str(target_userprofile.user.username) + ".")
            else:
                userprofile.following.add(target_userprofile)
                target_userprofile.update_reputation("ACTIVITY_SOCIAL_FOLLOW")
                messages.success(request, "You are now following " + str(target_userprofile.user.username) + ".")
                Activity.log_activity("ACTIVITY_SOCIAL_FOLLOW", userprofile, source=target_userprofile)
            return redirect (URL_USERPROFILE + str(target_userprofile.id))
    raise Http404

@login_required
def unfollow(request):
    if request.method == "POST":
        userprofile = request.user.userprofile
        target_userprofile_id = request.POST["target_userprofile_id"]
        target_userprofile = get_object_or_404(UserProfile, pk=target_userprofile_id)

        if userprofile.id != target_userprofile.id:
            if target_userprofile in userprofile.following.all():
                userprofile.following.remove(target_userprofile)
                target_userprofile.update_reputation("ACTIVITY_SOCIAL_UNFOLLOW")
                messages.success(request, "You are no longer following " + str(target_userprofile.user.username) + ".")
                Activity.log_activity("ACTIVITY_SOCIAL_UNFOLLOW", userprofile, source=target_userprofile)
                return redirect(URL_USERPROFILE + str(target_userprofile.id))
    raise Http404

@login_required
def message(request):
    if request.method == "POST":
        message = request.POST ["message"]
        target_userprofile_id = request.POST ["target_userprofile_id"]
        target_userprofile = get_object_or_404(UserProfile, pk=target_userprofile_id)
        from_userprofile = request.user.userprofile

        if len(message) > USERPROFILE_MESSAGE_LENGTH:
            messages.error(request, "Message size is too big. Please try again.")
            return redirect(URL_USERPROFILE + str(target_userprofile_id))

        if from_userprofile.id == target_userprofile.id:
            messages.error (request, "You cannot send a message to yourself.")
            return redirect(URL_USERPROFILE + str(from_userprofile.id))

        print_info_msg ("Sending an email message from %s to %s" % (from_userprofile.user.username, target_userprofile.user.username))
        completed = from_userprofile.send_email_message_to_UserProfile(target_userprofile, message, test_email=False)
        Activity.log_activity("ACTIVITY_SOCIAL_SEND_MESSAGE_TO_USER", from_userprofile, source=target_userprofile)
        messages.success(request, "You have successfully sent your message to %s" % target_userprofile.user.username + ".")
        return redirect(URL_USERPROFILE + str(target_userprofile_id))

@login_required
@allow_only_userprofile_owner
def edit(request, userprofile_id):
    if request.method == 'GET':
        profile = get_object_or_404(UserProfile, pk=userprofile_id)
        return render_to_response(HTML_EDITUSERPROFILE_FORM, {
            "form": UserProfileForm(instance=profile.user),
            "pic_url": profile.img_path,
            "password_form": PasswordChangeForm(request.user)
        }, RequestContext(request))
    else:
        raise Http404

@login_required
def update_info(request):
    if request.method == "POST":
        user = request.user
        profile = user.userprofile
        user_changed = email_changed = False
        #Hack to circumvent UserProfileForm validation.
        request.POST["password1"] = request.POST["password2"] = "TEST"
        request.POST["dob"] = profile.dob
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid() == False:
            return render_to_response(HTML_EDITUSERPROFILE_FORM, {
                "form": form,
                "pic_url": profile.img_path,
                "password_form": PasswordChangeForm(user)
            }, RequestContext(request))

        if request.FILES.get("img_path"): #Change the photo
            user_changed = True
            profile.set_images(request.FILES.get("img_path"), save=True, rotation=request.POST.get("img_rotation"))
            messages.success(request, "Looking good!")
            Activity.log_activity("ACTIVITY_USER_SET_PHOTO", profile)
            profile.update_reputation("ACTIVITY_USER_SET_PHOTO")

        if request.POST ["username"] != user.username: #Check if username has changed
            if UserProfile.get_UserProfile(username=request.POST["username"]) != None:
                messages.error(request, "Sorry, that username is already being used. Try another one.")
                return redirect(URL_EDITUSERPROFILE + str(profile.id))
            else:
                user.username = request.POST["username"]
                Activity.log_activity("ACTIVITY_USER_CHANGED_USERNAME", profile)
                user_changed = True

        if request.POST["email"] != user.email: #Check if email has changed.
            if UserProfile.get_UserProfile(email=request.POST["email"]) != None:
                messages.error(request, "Sorry, that email is already being used. Try another one.")
                return redirect(URL_EDITUSERPROFILE + str(profile.id))
            else:
                activation_key = create_sha1_hash(user.username)
                print_info_msg ('user: %s \tactivation-key: %s' % (user, activation_key))

                try: #Create a new EditUserProfile object for activating a new email address.
                    edit_userprofile = EditUserProfile.objects.get(user=user)
                except:
                    edit_userprofile = EditUserProfile()
                    edit_userprofile.user = user

                edit_userprofile.activation_key = activation_key
                edit_userprofile.new_email = request.POST["email"]
                edit_userprofile.date_of_change = datetime.now()
                edit_userprofile.save()
                #Prepare the email for verification.
                subject = render_to_string(TEXTFILE_EMAIL_CHANGE_SUBJECT, {})
                ctx = {
                    "site": Site.objects.get_current(),
                    "activation_key":activation_key,
                    "expiration_days":settings.ACCOUNT_ACTIVATION_DAYS
                }

                body = render_to_string(TEXTFILE_EMAIL_CHANGE_BODY, ctx)
                send_email(subject, body, None, [edit_userprofile.new_email])
                print_info_msg ("Sent email verification for %s" % user)
                user_changed = True
                email_changed = True

        if request.POST ["first_name"] != user.first_name: #First name check.
            user.first_name = request.POST["first_name"]
            user_changed = True
        if request.POST ["last_name"] != user.last_name: #Last name check.
            user.last_name = request.POST["last_name"]
            user_changed = True
        if request.POST ["description"] != profile.description: #Description check.
            profile.description = request.POST ["description"]
            user_changed = True
        if user_changed == True:
            user.save()
            profile.save()
            if email_changed == True:
                messages.success(request, "Your changes have been saved. Please check your email to find an email from us asking to verify your new email address.")
            else:
                messages.success(request, "Your changes have been saved.")
        else:
            messages.info(request, "Nothing was changed!")
        return redirect(URL_USERPROFILE + str(profile.id))
    else:
        raise Http404

@login_required
def update_password(request):
    if request.method == "POST":
        user = request.user
        old_password = request.POST ["old_password"]
        new_password = request.POST ["new_password1"]
        confirm_password = request.POST ["new_password2"]

        #First, check old password.
        if user.check_password(old_password) == False:
            messages.error(request, "Sorry, your old password was incorrect. Try again.")

        elif new_password != confirm_password:
            messages.error(request, "Please confirm your new password. Your new passwords don't match.")

        else:
            user.set_password(new_password)
            messages.success(request, "Your password has been changed successfully.")
            user.save()
        return redirect (URL_EDITUSERPROFILE + "%d/" % user.userprofile.id)
    else:
        raise Http404

@login_required
def delete(request):
    if request.method == "POST":
        profile = request.user.userprofile
        profile.delete()
        logout(request)
        messages.success(request, "Profile successfully deleted. Thank you for your help, and please come back soon!")
        return redirect(URL_HOME)
    else:
        raise Http404

@login_required
def email_verification_complete (request, activation_key):
    try:
        edituserprofile = EditUserProfile.objects.get(activation_key=activation_key)
        #If OK, then save the new email for the user and delete EditUserProfile object.
        if edituserprofile.activation_key_expired() == False:
            edituserprofile.user.email = edituserprofile.new_email
            edituserprofile.user.save()
            edituserprofile.delete()
            messages.success(request, "You have successfully updated your email address!")
        else:
            messages.error (request, "Sorry, Your activation key has expired.")
    except Exception as e:
        print_debug_msg(e)
        messages.error (request, "Sorry, that's an invalid activation key. Please try to verify your email address again.")

    return redirect(URL_HOME)
