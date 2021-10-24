from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# from .models import
#from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required #functionbased
from django.contrib.auth.mixins import LoginRequiredMixin #classbased
from dotenv import load_dotenv
import os
import requests
import pprint

load_dotenv()
TM_CONSUMER_KEY = os.getenv("TM_CONSUMER_KEY")
TM_CONSUMER_SECRET_KEY = os.getenv("TM_CONSUMER_SECRET_KEY")

city = 'Los Angeles'
state = 'CA'
size = 5
# startdate = '10-24-2021'
# genreId = 1
api_url = f'https://app.ticketmaster.com/discovery/v2/events.json?size={size}&city={city}&stateCode={state}&apikey={TM_CONSUMER_KEY}'
print(api_url)
r = requests.get(api_url)
pprint.pprint(r.json()['_embedded']['events'])
events_list = [x['name'] for x in r.json()['_embedded']['events']]
print(events_list)

# just in case/for aws thing if needed
# import uuid #random numbers for urls
# import boto3 to talk to aws

# Create your views here.
def home(request):
    return render(request, 'home.html')

