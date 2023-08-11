"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def test(param_dict):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        reviews = client['reviews']

        selector = {"dealership": 15}
        print(reviews.get_query_result(selector, raw_result=True))

        print(reviews.all_docs(include_docs=True))

    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

# test(param_dict)


def get_all_dealerships(param_dict):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        dealers = client['dealerships']

        result = dealers.all_docs(include_docs=True)
        print(result)
        return result

    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


def get_state_dealerships(param_dict, state):
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


def get_dealer_reviews(param_dict, id):
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


def post_dealer_review(param_dict, review):
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
get_dealer_reviews(param_dict, 15)
