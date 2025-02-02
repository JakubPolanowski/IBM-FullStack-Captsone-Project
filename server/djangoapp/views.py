from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import CarDealer, DealerReview, CarModel
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    elif request.method == "GET":
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    context = {}
    context["dealers"] = CarDealer.objects.all()

    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    dealer = get_object_or_404(CarDealer, pk=dealer_id)
    reviews = dealer.dealerreview_set.all()

    context["dealer"] = dealer
    context["reviews"] = reviews

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review


def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = request.POST

            car = CarModel.objects.get(pk=form["car"])

            review = {
                "name": f"{request.user.first_name} {request.user.last_name}",
                "dealership": CarDealer.objects.get(pk=dealer_id),
                "review": form["content"],
                "purchase": "purchasecheck" in form,
                "purchase_date": form["purchasedate"],
                "car_model": car,
                "car_make": car.car_make,
                "car_year": car.year,
            }

            DealerReview.objects.create(**review)

            return HttpResponseRedirect(reverse(
                viewname="djangoapp:dealer_details",
                args=(dealer_id,)
            ))

        else:
            dealer = get_object_or_404(CarDealer, pk=dealer_id)
            context = {
                "cars": CarModel.objects.all(),
                "dealer": dealer,
            }

            return render(request, "djangoapp/add_review.html", context)
    else:
        return redirect("/djangoapp/login")
