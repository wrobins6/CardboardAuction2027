from __future__ import absolute_import, unicode_literals
from celery import shared_task
from auction.models import Alter

@shared_task
def testscream(statement):
	scream = ("THE FOLLOWING IS BEING SCREAMED AT A DELAY: " +  str(statement) )
	return scream
	
@shared_task
def decidevictor(auction_id):
	newmessage = "The following auction has ended: " + Alter.objects.get(id=auction_id).name + " with id of " + str(auction_id)
	print(newmessage)
	return newmessage
