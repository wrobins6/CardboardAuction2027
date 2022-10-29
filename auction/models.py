from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Alter(models.Model):
    name = models.CharField(max_length=64)
    deadLine = models.DateTimeField()

class Bid(models.Model):
    amount = models.IntegerField()
    alter = models.ForeignKey(Alter, on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
