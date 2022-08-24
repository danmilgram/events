import django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as BaseUser, Group

# Create your models here.

class User(BaseUser):
    type = models.CharField(max_length=2, choices=(('CU', 'Customer'),('BU', 'Bussiness')))

class Room(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=(('PR', 'Private'),('PU', 'Public')))
    date = models.DateField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name



    
