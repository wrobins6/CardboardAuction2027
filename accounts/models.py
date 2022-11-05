from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    customer_id = models.SlugField(max_length = 64)
    USER_TYPE_CHOICES = (
    (1, "buyer"),
    (2,  "consigner"),
    (3, "curator")
    )
    user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES, default = 1)
