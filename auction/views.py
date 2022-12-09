from django.shortcuts import render, redirect

import stripe
import shippo

from secret import secret
from .models import Alter, Auction, Bid, Alter_Image
from django.utils import timezone
from . import tasks
import os
import base64

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
        "street1": "18 Glenview Ave",
        "city": "Southbridge",
        "state": "MA",
        "zip": "01550",
        "country": "US"
    }
    address_to = {
        "name": "Mr Hippo",
        "street1": "118 Pomfret Street",
        "street2": "Apartment 2W",
        "city": "Putnam",
        "state": "CT",
        "zip": "06260",
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
        "activeAuctions" : Auction.objects.filter(deadLine__gt = timezone.now()),
        "inactiveAuctions" : Auction.objects.filter(deadLine__lte = timezone.now())
    }
    return render(request, "home_page.html", values)

def auction_page(request):
    auction = Auction.objects.get(pk = request.GET['aid'])
    bids = Bid.objects.filter(auction = request.GET['aid'])
    expired = auction.deadLine <= timezone.now()
    images = Alter_Image.objects.filter(alter = auction.alter)
    imageB64 = []

    for image in images:
        tempPicture = image.picture
        imageB64.append(base64.standard_b64encode(tempPicture).decode()) #base64 string, call decode() since b64encode returns a bytes object and not a string

    print(len(imageB64))

    values = {
        "auction" : auction,
        "bids" : bids,
        "expired" : expired,
        "images" : imageB64
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
            auction = Auction.objects.get(pk=auctionID)
        except:
            return error_page(request, "Error getting Auction!")

        if auction.deadLine <= timezone.now():
            return error_page(request, "Auction has already ended")

        if numCents < auction.startAmount:
            return error_page(request, "Input bid amount is less than or equal to the starting price.")

        bids = Bid.objects.filter(auction = auction)
        currentHighest = bids.order_by('-amount').first()

        if currentHighest is not None:
            if numCents < currentHighest.amount + auction.minimumIncrement:
                return error_page(request, "Input bid amount is less than or equal to the current highest bid plus the minimum increment.")

        new_bid = Bid.objects.create(amount = cents, auction = auction, user = request.user)
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
	# converteddeadline = timezone.strptime(alterdeadline, '%Y-%m-%dT%H:%M')
	# totaltime = (converteddeadline - timezone.now()).total_seconds()
	# print(totaltime)
	#print(request.user)
	#print(newalter.consigner)

	newalter = Alter(name=altername, consigner=request.user)
	newalter.save()

	for alterImage in request.FILES.getlist("alterimage"):
		alterImageBytes = alterImage.read()
		newAlterImage = Alter_Image(picture = alterImageBytes, alter= newalter)
		newAlterImage.save()
	# tasks.decidevictor.apply_async( (newalter.id,), countdown=totaltime )
	return redirect('home_page')

# ----------------------
# --- CURATION VIEWS ---
# ----------------------

def ensure_curator(request):
    if (not request.user.is_authenticated): return False
    return request.user.user_type == 2 or request.user.user_type == 3

def pending_alters(request):
    if (not ensure_curator(request)): return redirect('home page')
    dict = {
        "results" : Alter.objects.filter(underManagement = False)
    }
    return render(request, "pending_alters.html", dict)

def works_under_management(request):
    if (not ensure_curator(request)): return redirect('home page')
    alters = Alter.objects.filter(underManagement = True)
    results = []
    for alter in alters:
        if (hasattr(alter, 'auction') and alter.auction is not None):
            pass
        else:
            results.append(alter)
    dict = {
        "results" : results
    }
    return render(request, "works_under_mangement.html", dict)

def accept_pending_alter(request):
    if (not ensure_curator(request)): return redirect('home page')
    if (request.method != 'POST'): return redirect('home_page')
    alter = Alter.objects.get(pk = request.POST['aid'])
    alter.underManagement = True
    alter.save()
    return redirect('pending_alters')

def setup_auction_page(request):
    if (not ensure_curator(request)): return redirect('home page')
    alter = Alter.objects.get(pk = request.GET['aid'])
    if (hasattr(alter, 'auction') and alter.auction is not None):
        return error_page(request, "An Auction already exists for this alter!")
    dict = {
        "alter" : alter
    }
    return render(request, "setup_auction_page.html", dict)

def setup_auction_action(request):
    if (not ensure_curator(request)): return redirect('home_page')
    if (request.method != 'POST'): return redirect('home_page')
    try:
        alterID = request.POST['aid']
        launchTime = request.POST['launchTime']
        deadLine = request.POST['deadLine']
        startAmount = request.POST['startAmount']
        minimumIncrement = request.POST['minimumIncrement']
    except:
        return error_page(request, "Setup missing key values!")
    alter = Alter.objects.get(pk = alterID)
    newAuction = Auction(
        alter=alter,
        startAmount=startAmount,
        minimumIncrement=minimumIncrement,
        launchTime=launchTime,
        deadLine=deadLine
        )
    newAuction.save()
    return redirect('home_page')
