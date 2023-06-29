from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=130)
    genre = models.CharField(max_length=30)
    rating = models.FloatField()
    popularity = models.IntegerField(default=5)
    year = models.IntegerField()
    synopsis = models.CharField(max_length=800)
    image = models.URLField()
    price = models.FloatField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    name = models.CharField(max_length=130)
    price = models.FloatField()
    user = models.ForeignKey(to= User, on_delete=models.CASCADE)
    movie = models.ForeignKey(to= Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Bill(models.Model):
    indian_states = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
    STATES = [(x,f" {x}") for x in indian_states]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15)
    Apartment_or_Building_number = models.CharField(max_length=200)
    Area_or_street = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    town_or_city = models.CharField(max_length=30) 
    state = models.CharField(max_length=50, choices = STATES)

