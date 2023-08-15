from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_all_dealerships, get_dealer_reviews, post_dealer_review
from .models import CarMake, CarModel
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
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

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

# # Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)
    
# def get_dealerships(request):

#     dealerships = get_all_dealerships(url, **kwargs)
#     dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
#     return dealer_names

def get_dealerships(request):
    context = {}
    context_object_name = 'dealerships'
    dealerships = get_all_dealerships(None)
    # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
    context.update({'dealerships': dealerships})
    # return HttpResponse(dealer_names)
    return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}

    # context_object_name = 'dealer_id'
    # context_object_name = 'dealer_name'
    # dealer_id = dealer_id

    # dealer_name = (dealer.id == dealer_id for dealer in get_all_dealerships(None))
    for dealer in get_all_dealerships(None):
        if dealer.id == dealer_id:
            dealer_name = dealer.full_name

    context_object_name = 'reviews'
    reviews = get_dealer_reviews(None, dealer_id)
    context.update({'reviews': reviews})
    context.update({'dealer_id': dealer_id})
    context.update({'dealer_name': dealer_name})
    review_text = ' '.join([review.review for review in reviews])
    return render(request, 'djangoapp/dealer_details.html', context)
    
def write_review(request, dealer_id):
    context = {}

    dealer_name = ""
    for dealer in get_all_dealerships(None):
        if dealer.id == dealer_id:
            dealer_name = dealer.full_name
    context.update({'dealer_name': dealer_name})
    context.update({'dealer_id': dealer_id})

    print(dealer_name)

    return render(request, "djangoapp/add_review.html", context)

def add_review(request, dealer_id):

    if request.method == "GET":
        context = {}

        dealer_name = ""
        for dealer in get_all_dealerships(None):
            if dealer.id == dealer_id:
                dealer_name = dealer.full_name
        context.update({'dealer_name': dealer_name})
        context.update({'dealer_id': dealer_id})

        cars = CarModel.objects.filter(dealerId=dealer_id)
        context.update({'cars': cars})

        return render(request, "djangoapp/add_review.html", context)

    if request.method == "POST":
        review = {}
        # review['id'] = 10
        # review['name'] = "name"
        # print("review['name']:", review['name'])
        # review["dealership"] = dealer_id
        # review["review"] = "heat death at the end of the universe"
        # review["purchase"] = True
        # review["purchase_date"] = datetime.utcnow().isoformat()
        # review["car_make"] = "Audi"
        # review["car_model"] = "A3"
        # review["car_year"] = 2020

        json_payload = {}
        json_payload["review"] = review
        # result = post_dealer_review(json_payload)
        # result = post_dealer_review(review)
        # print(result)

        print("request.POST:", request.POST)
        review['id'] = 10
        review['name'] = request.POST['name_text']
        review["dealership"] = dealer_id
        review["review"] = request.POST['review_text']
        if request.POST['purchasecheck'] == "Purchased":
            review["purchase"] = True
        else:
            review["purchase"] = False
        # review["purchase_date"] = datetime(request.POST['purchasedate']).isoformat()
        review["purchase_date"] = datetime.strptime(request.POST['purchasedate'], "%Y-%m-%d").isoformat()
        car = CarModel.objects.filter(dealerId=dealer_id)[int(request.POST['purchased_car']) - 1]
        review["car_make"] = car.carMake.name
        review["car_model"] = car.name
        review["car_year"] = car.year.strftime("%Y")
        print(review)

        result = post_dealer_review(review)
        print(result)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)