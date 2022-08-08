from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate

from djangoapp.models import CarModel
from . import restapis
import logging

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
        if user is None:
            messages.warning(request, "Invalid username or password")
        if not user is None:
            login(request, user)
    return redirect("djangoapp:index")


def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


def get_dealerships(request):
    context = {}
    context["dealerships"] = restapis.get_dealerships()
    return render(request, "djangoapp/index.html", context)


def get_dealer_details(request, dealer_id):
    context = {"dealer_id": dealer_id, "dealer": restapis.get_a_dealer(dealer_id)}
    reviews = restapis.get_dealer_reviews_from_cf(dealer_id)
    context["dealer_reviews"] = list(
        filter(lambda x: int(x.dealership) == int(dealer_id), reviews)
    )
    return render(
        request, template_name="djangoapp/dealer_details.html", context=context
    )


def add_review(request, dealer_id):
    context = {}
    if request.method == "POST":
        out = restapis.add_review(request, dealer_id)
        if not out:
            messages.warning(request, message="Error could not post review")
        else:
            messages.info(request, message="Review submitted successfully")
        return redirect("djangoapp:dealer_details", dealer_id)
    else:
        context["dealer"] = restapis.get_a_dealer(dealer_id)
        context["cars"] = CarModel.objects.filter(dealer_id=dealer_id)
        # for model in CarModel.objects.filter(dealer_id=dealer_id):
        #     for make in model.carmake.all():
        #         context["cars"].append(make)
    return render(request, template_name="djangoapp/add_review.html", context=context)
