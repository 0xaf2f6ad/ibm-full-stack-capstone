from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = "djangoapp"

urlpatterns = [
    # auth related routes
    path(route="main/register", view=views.registration_request, name="register"),
    path(route="main/login", view=views.login_request, name="login"),
    path(route="main/logout", view=views.logout_request, name="logout"),
    # general views
    path(route="", view=views.get_dealerships, name="index"),
    path(route="about", view=views.about, name="about"),
    path(route="contact", view=views.contact, name="contact"),
    path(
        route="dealer/<int:dealer_id>",
        view=views.get_dealer_details,
        name="dealer_details",
    ),
    path(
        route="review/<int:dealer_id>",
        view=views.add_review,
        name="add_review",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
