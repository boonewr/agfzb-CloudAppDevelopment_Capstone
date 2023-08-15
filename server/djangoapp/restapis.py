from cloudant.client import Cloudant
from cloudant.error import CloudantException
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import requests
import json
import os

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions


from dotenv import load_dotenv
load_dotenv()
token = os.environ.get("api-token")

param_dict = {
    "IAM_API_KEY": os.environ.get("IAM_API_KEY"),
    "COUCH_URL": os.environ.get("COUCH_URL"),
    "COUCH_USERNAME": os.environ.get("COUCH_USERNAME")
}
api_key = os.environ.get("NLU_API_KEY")


def get_all_dealerships(url, **kwargs):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        dealers = client['dealerships']

        result = dealers.all_docs(include_docs=True)
        # print(result)

        if result:
            results = []
            # print(result)
            # Get the row list in JSON as dealers
            dealers = result["rows"]
            # print("rows:", dealers)
            # For each dealer object
            for dealer in dealers:
                # Get its content in `doc` object
                dealer_doc = dealer["doc"]
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["state"], zip=dealer_doc["zip"])
                results.append(dealer_obj)

            return results

    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


def get_state_dealerships(state):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        dealers = client['dealerships']

        selector = {"state": state}
        result = dealers.get_query_result(selector, raw_result=True)

        print(result)
        return result

    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


def get_request(url, params, **kwargs):
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                auth=HTTPBasicAuth('apikey', api_key))
        print("response", response)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def analyze_review_sentiments(review):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/4daf55dd-5712-4eb1-91ea-9c427ae6b604"


    authenticator = IAMAuthenticator(api_key)

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(
        text=review,
        features=Features(
            entities=EntitiesOptions(emotion=False, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=False, sentiment=True,
                                    limit=2)),
        language='en'
        # features=Features()
    ).get_result()

    # print(json.dumps(response, indent=2))
    print(response, "\n")
    if response["keywords"]:
        sentiment_label = response["keywords"][0]["sentiment"]["label"] 
    else:
        sentiment_label = "error"
        print("error getting sentiment")
    return sentiment_label


def get_dealer_reviews(url, id, **kwargs):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        reviews = client['reviews']

        selector = {"dealership": id}
        result = reviews.get_query_result(selector, raw_result=True)

        if result:
            results = []
            # print(result)
            # Get the row list in JSON as dealers
            reviews = result["docs"]
            # For each dealer object
            for review in reviews:
                review_doc = review
                # print("ID SO FAR:", review_doc["id"])
                if review_doc["purchase"] == True:
                    review_obj = DealerReview(
                        dealership=review_doc["dealership"],
                        name=review_doc["name"],
                        purchase=review_doc["purchase"],
                        review=review_doc["review"],
                        purchase_date=review_doc['purchase_date'],
                        car_make=review_doc["car_make"],
                        car_model=review_doc["car_model"],
                        car_year=review_doc["car_year"],
                        id=review_doc["id"],
                        sentiment="Null"
                    )
                else:
                    review_obj = DealerReview(
                        dealership=review_doc["dealership"],
                        name=review_doc["name"],
                        purchase=review_doc["purchase"],
                        review=review_doc["review"],
                        purchase_date="Null",
                        car_make="Null",
                        car_model="Null",
                        car_year="Null",
                        id=review_doc["id"],
                        sentiment="Null"
                    )
                review_obj.sentiment = analyze_review_sentiments(
                    review_obj.review)
                results.append(review_obj)
            # print(results)
            # print("results:", results)
            return results

    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


def post_dealer_review(review):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        reviews = client['reviews']

        result = reviews.create_document(review)
        print(result)
        return result

    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


newReview = {
    "id": 1115,
    "name": "Uupkar Lidder",
    "dealership": 15,
    "review": "Great service!",
    "purchase": False,
    "another": "field",
    "purchase_date": "02/16/2021",
    "car_make": "Audi",
    "car_model": "Car",
    "car_year": 2021
}

# post_dealer_review(param_dict, review)
# get_dealer_reviews(param_dict, 15)
# get_all_dealerships()
