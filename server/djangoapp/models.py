import dataclasses
from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return f"Make : {self.name}"


class CarModel(models.Model):
    name = models.CharField(max_length=60)
    car_type = models.CharField(max_length=30)
    carmake = models.ManyToManyField(CarMake)
    dealer_id = models.IntegerField()
    year = models.DateField(default=now)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} |  {self.car_type} | {self.year}"


@dataclasses.dataclass
class CarDealer:
    docid: int
    id: int
    full_name: str
    short_name: str
    address: str
    zip: str
    city: str
    state: str
    lat: float
    long: float
    st: str


@dataclasses.dataclass
class DealerReview:
    id: str
    dealership: int
    name: str = "unknown"
    review: str = "unknown"
    purchase: str = "unknown"
    purchase_date: str = "unknown"
    car_make: str = "unknown"
    car_model: str = "unknown"
    car_year: str = "unknown"
    # watson related
    sentiment: str = "not-checked"
