from django.db import models
from django.urls import reverse
from datetime import datetime, date
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    event_id = models.CharField(max_length=50)
    def __str__(self):
        return self.event_id
    def get_absolute_url(self):
        return reverse('details', kwargs={'event_id': self.id})

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.user}-{self.event.all()[0].name}"
        return f'{self.user.user.username}-{self.event.name}'