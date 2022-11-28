from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Alter(models.Model):
    name = models.CharField(max_length=64)
    consigner = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null=True)
    underManagement = models.BooleanField(default=False)

class Auction(models.Model):
    alter = models.OneToOneField(Alter, on_delete = models.CASCADE, null=True)
    startAmount = models.IntegerField()
    minimumIncrement = models.IntegerField()
    launchTime = models.DateTimeField()
    deadLine = models.DateTimeField()
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)

class Bid(models.Model):
    amount = models.IntegerField()
    auction = models.ForeignKey(Auction, on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
