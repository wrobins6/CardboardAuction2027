from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def testscream(statement):
	scream = ("THE FOLLOWING IS BEING SCREAMED AT A DELAY: " +  str(statement) )
	return scream
