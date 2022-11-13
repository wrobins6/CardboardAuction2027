from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import logout, login, authenticate
from secret import secret
from auction.models import Alter
import stripe
import datetime

stripe.api_key = secret.getStripePrivateKey()

# Create your views here.

def login_page(request):
    return render(request, "login_page.html")
    
def login_action(request):
    if (request.method == 'POST'):
        logout(request)
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            print(user.username + " logged in.")
            return redirect("login_success")
        else:
            print("a loggin attempt failed")
            return redirect('login_failure')
    return redirect("login_page")

def register_page(request):
    values = {
        "pk" : secret.getStripePublicKey()
    }
    return render(request, "register_page.html", values)
    
def register_action(request):
    if (request.method == 'POST'):
        logout(request)
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        card_token = request.POST['stripeToken']

        customer = stripe.Customer.create(
            name = (first_name + " " + last_name),
            email = email,
            source = request.POST['stripeToken']
            )

        new_user = CustomUser.objects.create_user(
            username = username,
            email = email,
            password = password,
            first_name = first_name,
            last_name = last_name,
            customer_id = customer.id,
            user_type = 1
            )
    return redirect("home_page")
    
def login_success(request):
    if (request.user.is_authenticated):
        return render(request, "consignment_portal.html")
    else:
        return redirect("home_page")

def login_failure(request):
    return render(request, "home_page.html")

def logout_action(request):
    logout(request)
    return redirect("home_page")
	    

