from django.contrib import admin
from .models import CarModel, CarMake


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3


class CarModelAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


class CarMakeInline(admin.StackedInline):
    model = CarMake
    extra = 3


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarMakeInline]


admin.site.register(CarModel)
admin.site.register(CarMake)
