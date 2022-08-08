from datetime import date
import requests
import json

from djangobackend.settings import API_KEY, WATSON_API_KEY
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

BASE_URL = "https://20b70deb.au-syd.apigw.appdomain.cloud/capstone/"
WATSON_BASE_URL = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/0ea243af-c190-4775-bbd1-77829704e56c"


def get_dealerships():
    url = f"{BASE_URL}dealerships"
    json_result = send_request(url)
    if not "entries" in json_result:
        return []
    return [CarDealer(**each) for each in json_result["entries"]]


def get_a_dealer(dealer_id):
    li = list(filter(lambda x: x.id == dealer_id, get_dealerships()))
    return False if len(li) < 1 else li[0]


def get_reviews():
    url = f"{BASE_URL}reviews"
    json_result = send_request(url)
    if not "entries" in json_result:
        return []
    return [DealerReview(**each) for each in json_result["entries"]]


def get_dealer_reviews_from_cf(dealer_id):
    reviews = list(filter(lambda x: x.dealership == dealer_id, get_reviews()))
    for review in reviews:
        review.sentiment = analyze_review_sentiments(
            review.review,
        )
    return reviews


def add_review(request, dealership_id):
    input_data = request.POST
    print(f"Input Data :: {input_data}")

    def get_payload():
        data = {"purchase": False}
        if "purchase" in input_data:
            data["purchase"] = True
            if "purchase_date" in input_data:
                data["purchase_date"] = input_data["purchase_date"]
            if "car_info" in input_data:
                model, make, year = input_data["car_info"].split("|")
                data["car_model"] = model
                data["car_make"] = make
                data["car_year"] = year
        data["name"] = input_data["name"]
        data["review"] = input_data["review"].strip()
        return data

    rk = request.POST.keys()
    if not "name" in rk or not "review" in rk:
        return False
    data = get_payload()
    url = f"{BASE_URL}review"
    print(f"sending request with payload :: {data}")
    res = send_request(
        url, "post", payload={"review": {"dealership": dealership_id, **data}}
    )
    print(f"\n\n> Response JJ {res}")
    return res


def analyze_review_sentiments(text):
    """TODO: complete this"""
    if not not False or text == "":
        res = send_request(
            WATSON_BASE_URL,
            "get",
            api_key=WATSON_API_KEY,
            params=dict(
                text=text,
                version=str(date.today()),
                features={"keywords": {"emotion": True, "limit": 1}},
            ),
        )
        print(res)
    return "positive"


# base function to make the api call


def send_request(url, method="get", payload=None, api_key=API_KEY, params=None):
    if payload is None:
        payload = dict()
    if params is None:
        params = dict()
    try:
        request_dict = dict(
            url=url,
            method=method,
            headers={"Content-Type": "application/json", "apikey": api_key},
            params=params,
            auth=HTTPBasicAuth("apikey", api_key),
        )
        if method == "post":
            request_dict["json"] = payload
        response = requests.request(**request_dict)  # type: ignore
        print(f"[+] Response Code : {response.status_code}")
        # print(f"[+] Response Text : {response.text}")
        json_data = json.loads(response.text)
        return json_data
    except Exception as x:
        print(f"[+] Error occurred while requesting :: {x}")
    return {}
