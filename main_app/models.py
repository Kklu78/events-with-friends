from django.db import models
from django.urls import reverse
from datetime import datetime, date
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date = models.DateField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ManyToManyField(UserProfile)
    event = models.ManyToManyField(Event)
    content = models.TextField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.all()[0].user.username}-{self.event.all()[0].name}"
