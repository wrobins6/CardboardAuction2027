from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Alter
from .models import Bid
from .models import Auction

# Register your models here.
admin.site.register(Alter)
admin.site.register(Bid)
admin.site.register(Auction)