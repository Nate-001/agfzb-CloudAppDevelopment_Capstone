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
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth.decorators import login_required
import requests
#from flask import Flask, request, jsonify, abort




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
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            # If not, return to login page again
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect(request.META.get('HTTP_REFERER', '/'))

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
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://nathanieldro-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        
        # Create an empty context dictionary
        context = {}
        
        print(dealerships)

         # Create an empty context dictionary
        context = {'dealerships': dealerships}
        
        # Print the context to the console
        print("Context:", context)
        
        # Update the return statement to use render with the context
        return render(request, 'djangoapp/index.html', context)





# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    # Assuming you have a variable `url` representing the endpoint for dealer reviews
    url = "https://nathanieldro-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"

    # Call the get_dealer_reviews_from_cf method to retrieve reviews for the specified dealer_id
    reviews = get_dealer_reviews_from_cf(url, dealer_id)

    # Create a context dictionary to store the reviews
    context = {
        'dealer_id': dealer_id,
        'dealer_reviews': reviews,
    }

    # Print sentiment for each review
    for review in reviews:
        print(f"Review ID: {review.review_id}, Sentiment: {review.sentiment}")

    # Return the reviews in the HttpResponse
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Authentication required to add a review", status=401)

    # Handle GET request
    if request.method == 'GET':
        # Query cars with the dealer id to be reviewed
        # You need to replace this with your actual model and field names
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        
        # Append the queried cars into context
        context = {'cars': cars,'dealer_id': dealer_id}
        
        # Render the add_review.html template with the context
        return render(request, 'djangoapp/add_review.html', context)

    # Handle POST request
    elif request.method == 'POST':
        # Extract values from the review form
        review_content = request.POST.get('content')
        purchase_check = request.POST.get('purchasecheck')
        selected_car_id = request.POST.get('car')
        purchase_date = request.POST.get('purchasedate')

        # Query the selected car
        selected_car = CarModel.objects.get(id=selected_car_id)

        # Create a dictionary object for the review
        json_payload = {
            "id": dealer_id,  # Use the dealer_id as the review id, adjust as needed
            "name": request.user.username,  # Assuming the username is used as the name
            "dealership": dealer_id,
            "review": review_content,
            "purchase": purchase_check,
            "another": "field",  # Add other attributes as needed
            "purchase_date": datetime.utcnow().isoformat(),
            "car_make": selected_car.car_make.name,
            "car_model": selected_car.name,
            "car_year": selected_car.year.strftime("%Y"),
        }

        # Assuming you have a variable `url` representing the Flask API endpoint for posting reviews
        url = "https://nathanieldro-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"

        # Make a POST request to the Flask API endpoint
        response = post_request(url, json_payload, dealer_id=dealer_id)

        if response.status_code == 201:
            # Optionally, you can print the response to the console
            print(response.json())

            # Redirect user to the dealer details page
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            print("Error adding review. Status code:", response.status_code)
            print("Response content:", response.text)
            return HttpResponse("Error adding review", status=500)
