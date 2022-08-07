from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


def about(request):
    return render(request=request, template_name="static/about.html")


def contact(request):
    return render(request=request, template_name="static/contact.html")


def registration_request(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect("djangoapp:index")
        try:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            un = request.POST["un"]
            pwd = request.POST["pwd"]
        except Exception as e:
            logger.error(f"Some fields were not passed {e}")
            return redirect("djangoapp:register")
        if User.objects.filter(username=un).exists():
            return redirect("djangoapp:index")
        u = User(
            first_name=first_name,
            last_name=last_name,
            username=un,
        )
        u.set_password(pwd)
        u.save()
        user = authenticate(username=un, password=pwd)
        login(request, user)
        return redirect("djangoapp:index")
    return render(request=request, template_name="djangoapp/register.html")


def login_request(request):
    if request.method == "POST":
        un, pwd = request.POST["un"], request.POST["pwd"]
        user = authenticate(username=un, password=pwd)
        if not user is None:
            login(request, user)
    return redirect("djangoapp:index")


def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    # if request.method == "GET":
    #     return render(request, "djangoapp/index.html", context)
    return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    ...


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    ...
