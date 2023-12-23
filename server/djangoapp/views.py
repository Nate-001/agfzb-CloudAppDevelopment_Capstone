from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth.decorators import login_required
import requests
from flask import Flask, request, jsonify, abort



# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):

def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
#def contact(request):

def contact(request):
    return render(request, 'djangoapp/contact.html')

@csrf_protect
# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:get_dealer_details')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:get_dealer_details')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:get_dealer_details")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://nathanieldro-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.full_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)





# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    # Assuming you have a variable `url` representing the endpoint for dealer reviews
    url = "https://nathanieldro-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"

    # Call the get_dealer_reviews_from_cf method to retrieve reviews for the specified dealer_id
    reviews = get_dealer_reviews_from_cf(url, dealer_id)

    # Assuming you have a context variable named `context` to store the reviews
    context = {
        'dealer_reviews': reviews,
    }

    # Print sentiment for each review
    for review in reviews:
        print(f"Review ID: {review.review_id}, Sentiment: {review.sentiment}")

    # Return the reviews in the HttpResponse
    return HttpResponse(context['dealer_reviews'])

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Authentication required to add a review", status=401)

    # Create a dictionary object for the review
    json_payload  = {
        "id": dealer_id,  # Use the dealer_id as the review id, adjust as needed
        "name": request.user.username,  # Assuming the username is used as the name
        "dealership": dealer_id,
        "review": "This is a great car dealer",  # Replace with the actual review text
        "purchase": "Some purchase info",
        "another": "field",  # Add other attributes as needed
        "purchase_date": datetime.utcnow().isoformat(),
        "car_make": "Toyota",
        "car_model": "Camry",
        "car_year": 2022,
    }


    # Assuming you have a variable `url` representing the Flask API endpoint for posting reviews
    url = "https://nathanieldro-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"

    # Make a POST request to the Flask API endpoint
    response = post_request(url, json_payload, dealer_id=dealer_id)

    if response.status_code == 201:
        # Optionally, you can print the response to the console
        print(response.json())

        # Return the result of the post_request to the client
        return HttpResponse(response.text, status=response.status_code)
    else:
        return HttpResponse("Error adding review", status=500)