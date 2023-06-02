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
    name = models.CharField(max_length=30)
    price = models.FloatField()
    user = models.ForeignKey(to= User, on_delete=models.CASCADE)
    movie = models.ForeignKey(to= Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
