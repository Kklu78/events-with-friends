from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import *
from .forms import CommentForm
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

def home(request):
    return render(request, 'home.html')


def index(request):

    profile = UserProfile.objects.filter(user=request.user)
    
    events = Event.objects.filter(id__in = profile.values_list('events'))
    events_list = []
    for event_id in events:
        api = f'https://app.ticketmaster.com/discovery/v2/events.json?id={event_id}&apikey={TM_CONSUMER_KEY}'
        req = requests.get(api)
        s_events = req.json()['_embedded']['events'][0]
        s_events['images'] = sorted(s_events['images'], key = lambda x: (int(x['ratio']), int(x['width'])), reverse=True)
        events_list.append(s_events)
    return render(request, 'events/index.html', {'events': events_list})


def details(request, event_id):
    #query api
    api = f'https://app.ticketmaster.com/discovery/v2/events.json?id={event_id}&apikey={TM_CONSUMER_KEY}'
    r = requests.get(api)
    event = r.json()['_embedded']['events'][0]
    profile = UserProfile.objects.filter(user=request.user)
    userprofile = profile[0].id
    #if in user events
    user_events = Event.objects.filter(id__in = profile.values_list('events'))
    in_user_events = event_id in [x.event_id for x in user_events]

    comment_form = CommentForm()

    #generate attendees and comments if 
    event_obj = Event.objects.filter(event_id=event_id)
    if bool(event_obj):
        attendees = event_obj[0].userprofile_set.all()
        comments = event_obj[0].comment_set.all()[::-1]

        
        return render(request, 'events/details.html', {
            'event': event, 
            'in_user_events': in_user_events,
            'attendees': attendees,
            'comment_form': comment_form,
            'comments': comments,
            'userprofile':userprofile,
            })
    
    else:
        return render(request, 'events/details.html', {
        'event': event, 
        'in_user_events': in_user_events,
        'comment_form': comment_form,
        'userprofile': userprofile,
        })


# When viewing a specific event:
# I want to be able to add the event to My Saved Events


def add_event(request, event_id):
    # Create event into our database
    # Find the event
    # Try to save the event to a specific user's collection
    event = Event.objects.filter(event_id=event_id)   
    if bool(event):
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.events.add(event[0].id)
    else:
        api = f'https://app.ticketmaster.com/discovery/v2/events.json?id={event_id}&apikey={TM_CONSUMER_KEY}'
        r = requests.get(api)
        new_event = r.json()['_embedded']['events'][0]
        created_event = Event.objects.create(name=new_event['name'], event_id=event_id)
        # get the user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        # append the event to the userprofile's events
        user_profile.events.add(created_event.id)    
    return redirect('details', event_id=event_id)

def remove_event(request, event_id):
    event = Event.objects.filter(event_id=event_id)[0]
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.events.remove(event)
    return redirect('details', event_id=event_id)

    
# As a User, I want to be able to search for events in my area


def search(request):
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
        res_events = []
        for y in s_events:
            y['images'] = sorted(y['images'], key = lambda x: (int(x['ratio']), int(x['width'])), reverse=True)
            res_events.append(y)
    # redirect user to a page listing events in that search parameter
        return render(request, 'events/search.html', {'events': res_events, 'url': api_url, 'city': city})
    else:
        return render(request, 'events/search.html', {'events': None})


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

def add_comment(request, event_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.event_id = Event.objects.filter(event_id=event_id)[0].id
        new_comment.user_id = UserProfile.objects.get(user=request.user).id
        new_comment.created_date = datetime.now()
        new_comment.save()
    return redirect('details', event_id=event_id)

def delete_comment(request, event_id, comment_id):
    Comment.objects.filter(id=comment_id)[0].delete()
    return redirect('details', event_id=event_id)

