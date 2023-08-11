from cloudant.client import Cloudant
from cloudant.error import CloudantException
from .models import CarDealer
import requests
import os


from dotenv import load_dotenv
load_dotenv()
token = os.environ.get("api-token")

param_dict = {
    "IAM_API_KEY": os.environ.get("IAM_API_KEY"),
    "COUCH_URL": os.environ.get("COUCH_URL"),
    "COUCH_USERNAME": os.environ.get("COUCH_USERNAME")
}


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
            print(result)
            # Get the row list in JSON as dealers
            dealers = result["rows"]
            # For each dealer object
            for dealer in dealers:
                # Get its content in `doc` object
                dealer_doc = dealer["doc"]
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], zip=dealer_doc["zip"])
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


def get_dealer_reviews(id):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        reviews = client['reviews']

        selector = {"dealership": id}
        result = reviews.get_query_result(selector, raw_result=True)

        print(result)
        return result

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


review = {
    "id": 1114,
    "name": "Upkar Lidder",
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
