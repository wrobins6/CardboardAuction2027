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

def home_page(request):
    values = {
        "activeAuctions" : Alter.objects.filter(deadLine__gt = datetime.datetime.now()),
        "inactiveAuctions" : Alter.objects.filter(deadLine__lte = datetime.datetime.now())
    }
    return render(request, "home_page.html", values)

def alter_page(request):
    values = {
        "alter" : Alter.objects.get(pk = request.GET['aid']),
        "bids" : Bid.objects.filter(alter = request.GET['aid'])
    }
    return render(request, "alter_page.html", values)

def bid_action(request):
    if (request.method == 'POST'):
        if (not request.user.is_authenticated):
            return redirect("login_page")
        cents = request.POST['cents']
        alter = request.POST['alter']
        #customer = stripe.Customer.retrieve(request.user.customer_id)
        #charge = stripe.Charge.create(customer = customer, amount = cents, currency = 'usd', description = "Test Bid charge")
        new_bid = Bid.objects.create(amount = cents, alter_id = alter, user_id = request.user.pk)
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

