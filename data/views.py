from django.shortcuts import render
from django.contrib import messages
from main.views import contact
from data.models import Movie
from django.core.paginator import Paginator


# Create your views here.
def genre(request, genre):
    contact(request)
    movies = Movie.objects.filter(genre = genre)
    paginator = Paginator(movies, 4)
    current_page = request.GET.get("page")
    movies = paginator.get_page(current_page)
    return render(request, "data/generic.html", {"genre" : genre, "movies" : movies})