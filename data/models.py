from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=30)
    genre = models.CharField(max_length=30)
    rating = models.FloatField()
    year = models.IntegerField()
    synopsis = models.CharField(max_length=800)
    image = models.URLField()
    price = models.FloatField()

    def __str__(self):
        return self.name
    
    def __init__(self, name: str, genre: str, rating: float, year: int, synopsis: str, image: str, price: float) -> None:
        self.name = name
        self.genre = genre
        self.rating = rating
        self.year = year
        self.synopsis = synopsis
        self.image = image
        self.price = price
    
class Cart(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    user = models.ForeignKey(to= User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def __init__(self, name: str, price: float, user: User) -> None:
        self.name = name 
        self.price = price
        self.user = user

