from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from django.db.models import Min

from social_auth import __version__ as version
from social_auth.utils import setting

from models import Pets, PetReport
from random import choice, uniform



def home(request, include_ty=False):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        if request.method == 'POST':
            return update_pet(request)
        else:
            #if uniform(0, 1) <= 1:
            #   return disp_match(request, include_ty)
            #else:
            return disp_pet(request, include_ty)
    else:
        return HttpResponse("You are currently not authenticated. Please try again.")
        #return redirect('/epm')

def disp_match(request, include_ty = False):
    candidates = Pets.objects.filter(match = None)
    candidate = choice(candidates)
    context = {'pet_id' : candidate.id, 'pet' : candidate.entries[0], 'matching' : True, 'thankyou' : include_ty}
    return render_to_response('reporting/index.html', context, RequestContext(request))

def extract_pet(request):
    pet_id = request.POST['id']
    x = Pets.objects.get(id = pet_id)
    #just return the random one again for quick entry
    new = PetReport()
    x.revisions = x.revisions + 1
    new.img_useful = request.POST["img_useful"] == "True"
    new.lost = x.entries[-1].lost
    new.pet_type = x.entries[-1].pet_type
    new.img = x.entries[-1].img
    new.breed = request.POST["breed"]
    new.color = request.POST["color"]
    new.size = request.POST["size"]
    new.age = request.POST["age"]
    new.comments = request.POST["description"]
    return x, new


def update_pet(request):
    x, new = extract_pet(request)
    matching = False
    if request.POST['matching'] == "True":
        new.lost = not new.lost
        x.match = new
        matching = True
    else:
        x.entries.append(new)
    x.save()
    return disp_pet(request, True, None)#x.id if matching else None)

def disp_pet(request, include_ty=False, oid = None):
    """grab a random pet report among those with the least revisions and upvotes"""
    x = Pets.objects.all().aggregate(Min('revisions'))['revisions__min']
    #candidates = Pets.objects.filter(revisions = x).filter(match = None)
    if oid is None:
        candidates = Pets.objects.filter(revisions = x)
    else:
        candidates = Pets.objects.filter(id = oid)
    candidate = choice(candidates)
    context = {'pet_id' : candidate.id, 'pet' : candidate.entries[-1], 'matching' : False, 'thankyou' : include_ty}
    return render_to_response('reporting/index.html', context, RequestContext(request))

def upvote(request, pet_id):
    x = Pets.objects.get(id = pet_id)
    x.entries[-1].upvotes.append(request.user.username)
    x.revisions = x.revisions + 1
    x.save()
    return redirect('/epm/reporting')
