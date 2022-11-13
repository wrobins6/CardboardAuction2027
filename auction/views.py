from django.shortcuts import render, redirect
import stripe
from secret import secret
from .models import Alter
from .models import Bid
import datetime
from . import tasks

stripe.api_key = secret.getStripePrivateKey()



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
        "activeAuctions" : Alter.objects.filter(deadLine__gt = datetime.datetime.now()),
        "inactiveAuctions" : Alter.objects.filter(deadLine__lte = datetime.datetime.now())
    }
    return render(request, "home_page.html", values)

def alter_page(request):
    alter = Alter.objects.get(pk = request.GET['aid'])
    bids = Bid.objects.filter(alter = request.GET['aid'])

    expired = alter.deadLine <= datetime.datetime.now()

    values = {
        "alter" : alter,
        "bids" : bids,
        "expired" : expired
    }

    return render(request, "alter_page.html", values)

def bid_action(request):
    if (request.method == 'POST'):
        if (not request.user.is_authenticated):
            return redirect("login_page")
        try:
            cents = request.POST['cents']
            alterID = request.POST['alter']
        except:
            return error_page(request, "Bid missing key values!")

        numCents = int(cents)

        if numCents <= 0:
            return error_page(request, "Bid is less than or equal to zero!")

        try:
            alter = Alter.objects.get(id=alterID)
        except:
            return error_page(request, "Error getting Alter!")

        if alter.deadLine <= datetime.datetime.now():
            return error_page(request, "Auction has already ended")


        bids = Bid.objects.filter(alter = alter)
        currentHighest = bids.order_by('-amount').first()

        if numCents <= currentHighest:
            return error_page(request, "Input bid amount is less than or equal to the current highest bid")

        new_bid = Bid.objects.create(amount = cents, alter_id = alterID, user_id = request.user.pk)
    return redirect("home_page")

def search_action(request):
    values = {
        "alters" : Alter.objects.filter(name__contains = request.POST['search'])
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
	alterdesc = request.POST["alterdesc"]
	alterdeadline = request.POST["alterdeadline"]
	converteddeadline = datetime.datetime.strptime(alterdeadline, '%Y-%m-%dT%H:%M')
	
	totaltime = (converteddeadline - datetime.datetime.now()).total_seconds()
	print(totaltime)
	
	newalter = Alter(name=altername, deadLine=alterdeadline)
	newalter.save()
	tasks.decidevictor.apply_async( (newalter.id,), countdown=totaltime )
	
	return redirect('home_page')

