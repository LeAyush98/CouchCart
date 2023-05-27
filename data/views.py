from django.shortcuts import render
from django.contrib import messages
from main.views import contact
from data.models import Movie
from data.db_maker import add_data


# Create your views here.
def genre(request, genre):
    contact(request)
    movies = Movie.objects.all()
    return render(request, "data/generic.html", {"genre" : genre, "movies" : movies})