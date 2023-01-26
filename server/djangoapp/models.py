from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    WAGON = 'wagon'
    SUV = 'suv'
    TYPE_CHOICES = [
        (SEDAN, 'sedan'),
        (WAGON, 'wagon'),
        (SUV, 'suv')
        ]

    car_model = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=SEDAN)
    car_year = models.DateField(default=now)

    def __str__(self):
        return "Dealer ID: " + self.dealer_id + "Type: " + self.car_type

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, dealership, purchase, review, name="None", purchase_date="None", car_make="None", car_model="None", car_year="None"):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = "None"

    def __str__(self):
        return "Dealer review: " + self.review + ", Sentiment is: " + self.sentiment
