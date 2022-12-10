from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Auction
from .models import Alter
from .models import Bid
from accounts.models import CustomUser
from django.db.models import Max
from secret import secret
import stripe

stripe.api_key = secret.getStripePrivateKey()


def err(the_error):
	print(" --- ERROR! --- ")
	print(the_error)
	print(" -------------- ")
	return(the_error)
	
@shared_task
def decidevictor(auction_id):
	# Get Alter that just ended
	auction_won = Auction.objects.get(id=auction_id)
	if (auction_won is None):
		return err("No auctions with auction ID")
	print(str(auction_won.alter.name))
	
	# Get list of Bids on that auction
	bids = Bid.objects.filter(auction=auction_won)
	if (bids is None):
		return err("Bids came up as None")
	print(str(bids))
	
	# Get the victor bid of the alter
	bid_victor = bids.order_by('-amount').first()
	if (bid_victor is None):
		return err("No bid victor found")
	print(str(bid_victor))
	
	# Get the victor user of the alter
	user_victor = bid_victor.user
	if (user_victor is None):
		return err("No user victor found")
	print(str(user_victor))
	
	# Print info block
	new_message = "The following auction has ended: " + auction_won.alter.name + " with id of " + str(auction_id)
	print(new_message)
	victory_message = "The card was sold for " + str(bid_victor.amount) + " to " + user_victor.username
	print(victory_message)
	
	# Charge the user
	cents = bid_victor.amount
	customer = stripe.Customer.retrieve(user_victor.customer_id)
	if (customer is None): return err("There is no stripe customer for this user!")
	charge = stripe.Charge.create(
		customer = customer,
		amount = cents,
		currency = 'usd',
		description = "Test Charge"
	)
	
	return "Done!"
