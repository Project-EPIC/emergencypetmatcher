# Create your views here.

from django.shortcuts import render_to_response
from models import GFTEntry
from gftclient.authorization.clientlogin import ClientLogin
from gftclient.sql.sqlbuilder import SQL
from gftclient import ftclient
from datetime import datetime

def index(request):
    return render_to_response('gft/index.html', {})

def submit(request):
    if request.method == 'POST':
        form = GFTEntry(request.POST)
        if form.is_valid():
            name = str(form.cleaned_data['pet_name'])
            contact = str(form.cleaned_data['contact'])
            lostfound = form.cleaned_data['lostfound']
            lost = str(datetime.now()) if lostfound else ""
            found = str(datetime.now()) if not lostfound else ""
            tags = str(form.cleaned_data['tags'])
            lat = str(form.cleaned_data['latitude'])
            longitude = str(form.cleaned_data['longitude'])
            photo = str(form.cleaned_data['photograph'])
            #gft
            username="epicdatascouts@gmail.com"
            password="crowdsourcing"
            token = ClientLogin().authorize(username, password)
            ft_client = ftclient.ClientLoginFTClient(token)
            tid = 2038141
            rowdata = {'Pet Name':name, 'Tags':tags, 'Contact':contact, "Latitude":lat, "Longitude":longitude, "Lost":lost, "Found":found, "Photograph":photo}
            ft_client.query(SQL().insert(tid, rowdata))
        return render_to_response('gft/thanks.html', {'gft':form})

