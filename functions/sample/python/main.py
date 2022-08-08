from cloudant.client import Cloudant
from cloudant.error import CloudantException
from ibmcloudant import CloudantV1
import requests


def main(dict):
    c = CloudantV1.new_instance()
    c.set_service_url(dict["COUCH_URL"])
    for each in c.post_all_docs("reviews").get_result().json():
        ...

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
