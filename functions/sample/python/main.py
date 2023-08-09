"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

couch_username = os.getenv("COUCH_USERNAME")
iam_api_key = os.getenv("IAM_API_KEY")

print("Loading function")


def main(param_dict):
    print("Connecting to Cloudant")
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    # try:
    #     client = Cloudant.iam(
    #         account_name=couch_username,
    #         api_key=iam_api_key,
    #         connect=True,
    #     )
    #     print(f"Databases: {client.all_dbs()}")
    # except CloudantException as cloudant_exception:
    #     print("unable to connect")
    #     return {"error": cloudant_exception}
    # except (requests.exceptions.RequestException, ConnectionResetError) as err:
    #     print("connection error")
    #     return {"error": err}

    # print({"dbs": client.all_dbs()})
    # return {"dbs": client.all_dbs()}

main()