from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=25)
    description = models.TextField()

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=60)
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    SPORT = "Sport"
    HATCHBACK = "Hatchback"
    VAN = "Van"
    TRUCK = "Truck"
    OTHER = "Other"
    CAR_CHOICES = [
        (SEDAN, "Sedan"), (SUV, "SUV"),
        (WAGON, "Station wagon"), (SPORT, "Sports Car"),
        (HATCHBACK, "Hatchback"), (TRUCK, "Truck"),
        (OTHER, 'Other'),
    ]

    car_model = models.CharField(
        choices=CAR_CHOICES, default=SEDAN, max_length=25)
    year = models.DateField()

    def __str__(self):
        return f"Name: {self.name}, Year: {self.year}, Model: {self.car_model}"


class CarDealer(models.Model):
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    st = models.CharField(max_length=2)
    address = models.TextField()
    zip = models.CharField(max_length=25)
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=25)
    full_name = models.TextField()


class DealerReview(models.Model):
    name = models.CharField(max_length=25)
    dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    review = models.TextField()
    purchase = models.BooleanField()
    purchase_date = models.DateField()
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_year = models.IntegerField()


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
