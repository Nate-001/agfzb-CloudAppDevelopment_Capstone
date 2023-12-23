import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth




# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    if api_key:
        # Basic authentication GET
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                auth=HTTPBasicAuth('apikey', api_key))
    else:
        # No authentication GET
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})

    # Check the status code of the response
    status_code = response.status_code
    print(f"With status {status_code}")

    # Try to parse the response as JSON
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        # If parsing fails, return the raw text response
        return response.text

# Example usage:
# result = get_request("https://example.com/api/data", api_key="your_api_key", param1="value1", param2="value2")



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=json_payload, headers=headers, params=kwargs)

    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
# - Now, open the restapis.py file and in the ‘get_dealers_from_cf’ function, replace this previous line, which appears as follows:
# - dealer_doc = dealer[“doc”]
# - with this new line below:
# - dealer_doc = dealer
# - This will update the way the dealer_doc variable retrieves the content from the dealer object.
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # If the result is a list, use it directly
        if isinstance(json_result, list):
            dealers = json_result
        # If the result is a dictionary, get the "rows" key
        elif isinstance(json_result, dict):
            dealers = json_result.get("rows", [])
        else:
            dealers = []
        
        # For each dealer object
        for dealer in dealers:
            print(f"Dealer type: {type(dealer)}, Dealer content: {dealer}")
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # If the result is a list, use it directly
        if isinstance(json_result, list):
            dealers = json_result
        # If the result is a dictionary, get the "rows" key
        elif isinstance(json_result, dict):
            dealers = json_result.get("rows", [])
        else:
            dealers = []
        
        # For each dealer object
        for dealer in dealers:
            print(f"Dealer type: {type(dealer)}, Dealer content: {dealer}")
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results


def get_dealer_by_id(url, state, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # If the result is a list, use it directly
        if isinstance(json_result, list):
            dealers = json_result
        # If the result is a dictionary, get the "rows" key
        elif isinstance(json_result, dict):
            dealers = json_result.get("rows", [])
        else:
            dealers = []
        
        # For each dealer object
        for dealer in dealers:
            print(f"Dealer type: {type(dealer)}, Dealer content: {dealer}")
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    # Call get_request with a URL parameter and dealerId
    json_result = get_request(f"{url}?id={dealer_id}", **kwargs)
    results = []

    if json_result:
        # If the result is a list, use it directly
        if isinstance(json_result, list):
            reviews = json_result
        # If the result is a dictionary, get the "reviews" key
        elif isinstance(json_result, dict):
            reviews = json_result.get("reviews", [])
        else:
            reviews = []

        # For each review object
        for review in reviews:
            print(f"Review type: {type(review)}, Review content: {review}")
            # Get its content in `review_doc` object
            review_doc = review
            # Create a DealerReview object with values in `review_doc` object
            review_obj = DealerReview(
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                sentiment=analyze_review_sentiments(review_doc["review"]),  # Provide sentiment here
                review_id=review_doc["id"]
            )


            # Assign sentiment using Watson NLU
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
import requests
from requests.auth import HTTPBasicAuth

def analyze_review_sentiments(text):
    # Assuming you have the Watson NLU API endpoint and API key
    nlu_url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/4629c9ad-a213-4177-ae7d-a5cd6903f06c"
    api_key = "Yw71R_hbT1sgRBll6vHjtzsFF3iYznnCaGnWgBNjx5lr"

    # Set the parameters for the NLU API request
    params = {
        'version': '2021-08-01',
        'features': 'sentiment',
        'return_analyzed_text': True,
        'text': text,
    }

    # Make a call to the Watson NLU API endpoint with the specified parameters
    response = requests.get(nlu_url, params=params, headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth('apikey', api_key))

    # Extract sentiment label from the response
    sentiment_label = response.json().get('sentiment', {}).get('document', {}).get('label', 'Unknown')

    return sentiment_label

# Example usage:
# sentiment_result = analyze_review_sentiments("This is a positive review.")
# print(sentiment_result)
