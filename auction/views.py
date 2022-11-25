from django.shortcuts import render, redirect

import stripe
import shippo

from secret import secret
from .models import Alter, Auction, Bid
import datetime
from . import tasks

stripe.api_key = secret.getStripePrivateKey()
shippo.config.api_key = secret.getShippoSecretKey()


# ----------------------
# -- DEBUG VIEWS -------
# ----------------------

def testpay_page(request):
    return render(request, "testpay_page.html")
       
def testpay_action(request):
    if (request.method == 'POST'):
        if (not request.user.is_authenticated):
            return redirect("login_page")
        cents = request.POST['cents']
        customer = stripe.Customer.retrieve(request.user.customer_id)
        charge = stripe.Charge.create(
            customer = customer,
            amount = cents,
            currency = 'usd',
            description = "Test Charge"
            )
    return redirect("testpay_page")
    
def testship_page(request):
    return render(request, "testship_page.html")

def testship_action(request):
    address_from = {
        "name": "Shawn Ippotle",
        "street1": "215 Clayton St.",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94117",
        "country": "US"
    }
    address_to = {
        "name": "Mr Hippo",
        "street1": "8098",
        "city": "Glen Cove",
        "state": "NJ",
        "zip": "11542",
        "country": "US"
    }
    parcel = {
        "length": "5",
        "width": "5",
        "height": "5",
        "distance_unit": "in",
        "weight": "2",
        "mass_unit": "lb"
    }
    shipment = shippo.Shipment.create(
        address_from = address_from,
        address_to = address_to,
        parcels = [parcel]
    )
    rate = shipment.rates[0]
    transaction = shippo.Transaction.create(
        rate=rate.object_id,
        label_file_type="PDF"
    )
    if transaction.status == 'SUCCESS':
        print('Tracking URL: ' + transaction.tracking_url_provider)
        print('Shipping Label URL: ' + transaction.label_url)
    else:
        print(transaction.messages)
    return redirect("home_page")


# ----------------------
# -- GENERAL VIEWS -----
# ----------------------

def error_page(request, error):
    values = {
        "error" : error
    }
    return render(request, "error_page.html", values)

def home_page(request):
    values = {
        "activeAuctions" : Auction.objects.filter(deadLine__gt = datetime.datetime.now()),
        "inactiveAuctions" : Auction.objects.filter(deadLine__lte = datetime.datetime.now())
    }
    return render(request, "home_page.html", values)

def auction_page(request):
    auction = Auction.objects.get(pk = request.GET['aid'])
    bids = Bid.objects.filter(auction = request.GET['aid'])

    expired = Auction.deadLine <= datetime.datetime.now()

    values = {
        "auction" : auction,
        "alter" : auction.alter,
        "bids" : bids,
        "expired" : expired
    }

    return render(request, "auction_page.html", values)

def bid_action(request):
    if (request.method == 'POST'):
        if (not request.user.is_authenticated):
            return redirect("login_page")
        try:
            cents = request.POST['cents']
            auctionID = request.POST['auction']
        except:
            return error_page(request, "Bid missing key values!")
            
        numCents = int(cents)

        if numCents <= 0:
            return error_page(request, "Bid is less than or equal to zero!")

        try:
            auction = auction.objects.get(id=auctionID)
        except:
            return error_page(request, "Error getting Auction!")

        if auction.deadLine <= datetime.datetime.now():
            return error_page(request, "Auction has already ended")

        bids = Bid.objects.filter(auction = auction)
        currentHighest = bids.order_by('-amount').first()

        if numCents <= currentHighest:
            return error_page(request, "Input bid amount is less than or equal to the current highest bid")

        new_bid = Bid.objects.create(amount = cents, alter_id = auctionID, user_id = request.user.pk)
    return redirect("home_page")

def search_action(request):
    values = {
        "auctions" : Auction.objects.filter(alter__name__contains = request.POST['search'])
    }
    return render(request, "search_page.html", values)


# ----------------------
# - CONSIGNMENT VIEWS --
# ----------------------
  
def update_to_consigner(request):
    if (not request.user.is_authenticated):
        return redirect("login_page")
    else:
        print("Update the user to consigner group")
        request.user.user_type = 2
        request.user.save()
        return redirect("consignment_portal")

def consignment_page(request):
    return render(request, "consignment_page.html")

def consignment_portal(request):
    if (not request.user.is_authenticated):
        return redirect("login_page")
    else:
        return render(request, "consignment_portal.html")
        
def consignment_action(request):
	if (not request.user.is_authenticated):
		return redirect("login_page")
	if (not request.method == "POST"):
		return redirect("consignment_portal")
	altername = request.POST["altername"]
	# alterdesc = request.POST["alterdesc"]
	# alterdeadline = request.POST["alterdeadline"]
	# converteddeadline = datetime.datetime.strptime(alterdeadline, '%Y-%m-%dT%H:%M')
	# totaltime = (converteddeadline - datetime.datetime.now()).total_seconds()
	# print(totaltime)
	newalter = Alter(name=altername)
	newalter.save()
	# tasks.decidevictor.apply_async( (newalter.id,), countdown=totaltime )
	return redirect('home_page')

# ----------------------
# -- CURATION VIEWS  ---
# ----------------------

def pending_alters(request):
    return redirect('home_page')

def works_under_management(request):
    return redirect('home_page')

def accept_pending_alter(request):
    return redirect('home_page')

def alter_detail_page(request):
    return redirect('home_page')