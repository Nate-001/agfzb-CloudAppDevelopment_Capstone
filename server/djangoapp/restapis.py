import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


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
    json_results = get_request(url, **kwargs)

    dealers = []
    for result in json_results:
        dealer = CarDealer(
            dealer_id=result.get('_id'),
            name=result.get('name'),
            city=result.get('city'),
            state=result.get('state'),
            address=result.get('address'),
            zip_code=result.get('zip'),
            lat=result.get('lat'),
            long=result.get('long'),
            short_name=result.get('short_name'),
            full_name=result.get('full_name')
        )
        dealers.append(dealer)

    return dealers

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


