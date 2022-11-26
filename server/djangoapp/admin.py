from django.contrib import admin
from .models import CarModel, CarMake, CarDealer, DealerReview


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel


class CarDealerInline(admin.StackedInline):
    model = CarDealer


class CarMakeInline(admin.StackedInline):
    model = CarMake

# CarModelAdmin class


class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'name', 'dealer_id', 'car_model', 'year']
    list_filter = ['car_model', 'car_make', 'dealer_id', 'year',]
    search_fields = ['car_make', 'name']

# CarMakeAdmin class with CarModelInline


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]


class CarDealerAdmin(admin.ModelAdmin):
    search_fields = ["city", "state", "short_name", "long_name"]


    # Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarDealer, CarDealerAdmin)
admin.site.register(DealerReview, admin.ModelAdmin)
