from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import *
#from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required  # functionbased
from django.contrib.auth.mixins import LoginRequiredMixin  # classbased
from dotenv import load_dotenv
import os
import requests
import pprint


load_dotenv()
TM_CONSUMER_KEY = os.getenv("TM_CONSUMER_KEY")
TM_CONSUMER_SECRET_KEY = os.getenv("TM_CONSUMER_SECRET_KEY")


# city = 'Los Angeles'
# # state = 'CA'

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
    # As a User, I want to view my saved Events.
    # find profile
    profile = UserProfile.objects.filter(user=request.user)
    print(profile)
    print(profile.__dict__)
    events = profile.events.all()#.values_list('event_id')
    events_list = []
    for event_id in events:
        api = f'https://app.ticketmaster.com/discovery/v2/events.json?id={event_id}&apikey={TM_CONSUMER_KEY}'
        req = requests.get(api)
        s_events = req.json()['_embedded']['events']
        events_list.append(s_events)
    return render(request, 'events/index.html', {'events': events_list})


def details(request, event_id):
    print(request.user.id)
    api = f'https://app.ticketmaster.com/discovery/v2/events.json?id={event_id}&apikey={TM_CONSUMER_KEY}'
    r = requests.get(api)
    event = r.json()['_embedded']['events'][0]
    # event_id = event.id
    return render(request, 'events/details.html', {'event': event})

# When viewing a specific event:
# I want to be able to add the event to My Saved Events


def add_event(request, event_id):
    # Create event into our database
    # Find the event
    # Try to save the event to a specific user's collection
    api = f'https://app.ticketmaster.com/discovery/v2/events.json?id={event_id}&apikey={TM_CONSUMER_KEY}'
    r = requests.get(api)
    event = r.json()['_embedded']['events'][0]
    name = event.name
    Event.objects.create(name=name, event_id=event_id)
    # get the user's profile
    user_profile = UserProfile.objects.get(id=request.user.id)
    # append the event to the userprofile's events
    user_profile.events.add(event_id)

# As a User, I want to be able to search for events in my area


def search(request):
    events = None
    print(request.POST)
    print(bool(request.POST))
    if bool(request.POST) == True:
        # Change the city variable to the variable the user posted
        city = request.POST.get('city').split(', ')[0]
        state = request.POST.get('city').split(', ')[1]
        size = 7
    # have api url replace keys with correct locations
        api_url = f'https://app.ticketmaster.com/discovery/v2/events.json?size={size}&city={city}&stateCode={state}&apikey={TM_CONSUMER_KEY}'
    # grab events
        req = requests.get(api_url)
        s_events = req.json()['_embedded']['events']
    # redirect user to a page listing events in that search parameter
        return render(request, 'events/search.html', {'events': s_events, 'url': api_url, 'city': city})
    else:
        return render(request, 'events/search.html', {'events': events})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # form object that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            UserProfile.objects.create(user=user)
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form,
      'error_message': error_message
    })
