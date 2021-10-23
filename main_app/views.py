from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
import pprint
# Create your views here.
load_dotenv()
TM_CONSUMER_KEY = os.getenv("TM_CONSUMER_KEY")
TM_CONSUMER_SECRET_KEY = os.getenv("TM_CONSUMER_SECRET_KEY")

city = 'Los Angeles'
state = 'CA'
size = 2
api_url = f'https://app.ticketmaster.com/discovery/v2/events.json?size={size}&city={city}&stateCode={state}&apikey={TM_CONSUMER_KEY}'
print(api_url)
r = requests.get(api_url)
pprint.pprint(r.json())