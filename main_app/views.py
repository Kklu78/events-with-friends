from django.shortcuts import render, redirect
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


# city = 'Los Angeles'
# # state = 'CA'
size = 5
# # startdate = '10-24-2021'
# # genreId = 1
# api_url = f'https://app.ticketmaster.com/discovery/v2/events.json?size={size}&city={city}&stateCode={state}&apikey={TM_CONSUMER_KEY}'
# print(api_url)
# r = requests.get(api_url)
# pprint.pprint(r.json()['_embedded']['events'])
# events_list = [x['name'] for x in r.json()['_embedded']['events']]
# print(events_list)

# just in case/for aws thing if needed
# import uuid #random numbers for urls
# import boto3 to talk to aws

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'events/index.html')

# As a User, I want to view the details of a specific event
# When viewing a specific event:
    # I want to be able to see comments by most recent
    # I want to be able to add the event to My Saved Events
    # If the Event is already saved, I want to be able to remove it from my Saved Events
    # If the Event is already saved, I want to be able to make a comment on the Event
    # I want to be able to see the other Users have saved the Event, if any
def details(request):
    api = f'https://app.ticketmaster.com/discovery/v2/events.json?id=G5eYZpsTieYU_&apikey={TM_CONSUMER_KEY}'
    r = requests.get(api)
    event = r.json()['_embedded']['events'][0]
    return render(request, 'events/details.html', {'event':event})


# As a User, I want to be able to search for events in my area
def search(request):
    return render(request, 'events/search.html')

def start_search(request):
    # Change the city variable to the variable the user posted
    city = request.POST.get('city')
    print(city)
    # set state depending on city
    if city == 'Austin':
        state = 'TX'
    elif city == 'Seattle':
        state = 'WA'
    elif city == 'Boston':
        state = 'MA'
    elif city == 'Chicago':
        state = 'IL'
    elif city == 'New York':
        state = 'NY'
    elif city == 'Miami':
        state = 'FL'
    else:
        state = 'CA'
    # have api url replace keys with correct locations
    api_url = f'https://app.ticketmaster.com/discovery/v2/events.json?size={size}&city={city}&stateCode={state}&apikey={TM_CONSUMER_KEY}'
    # grab events
    req = requests.get(api_url)
    events = req.json()['_embedded']['events']
    # redirect user to a page listing events in that search parameter
    return render(request, 'main_app/event_list.html', {'events': events, 'url': api_url})
