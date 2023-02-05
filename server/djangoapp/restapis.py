import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
import requests
import json

def get_request(url, headers={'Content-Type': 'application/json'}, params=None, auth=None):
    try:
        response = requests.get(url, headers=headers, params=params, auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
        return None


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    print(response.status_code)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result['body']["rows"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        reviews = json_result['body']["docs"]
        if reviews:
            for i in [1]:
                review_doc = reviews[0]
                try:
                    review_obj = DealerReview(id=review_doc["id"], dealership=review_doc["dealership"], name=review_doc["name"],
                                    purchase=review_doc["purchase"], review=review_doc["review"], purchase_date=review_doc["purchase_date"],
                                    car_make=review_doc["car_make"],
                                    car_year=review_doc["car_year"], car_model=review_doc["car_model"])
                except:
                    review_obj = DealerReview(id=review_doc["id"], dealership=review_doc["dealership"],
                                    purchase=review_doc["purchase"], review=review_doc["review"])    
                results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = 'https://api.au-syd.language-translator.watson.cloud.ibm.com/instances/b0de95df-4984-434f-8832-e0eb4a435d4e'
    api_key = 'TAhb2rXghuMMZ8uU8OSx_yM_3G1o1apGBXnnm8g9BdmD'

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
    text=dealerreview,
    features=Features(sentiment=SentimentOptions(document=True))).get_result()

    return response["sentiment"]["label"]
