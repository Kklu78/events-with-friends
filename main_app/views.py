from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# from .models import
#from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required #functionbased
from django.contrib.auth.mixins import LoginRequiredMixin #classbased

# just in case/for aws thing if needed
# import uuid #random numbers for urls
# import boto3 to talk to aws

# Create your views here.
def home(request):
    return render(request, 'home.html')