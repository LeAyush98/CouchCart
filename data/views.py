from django.shortcuts import render
from django.contrib import messages
from main.views import contact
from data.models import Movie
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def genre(request, genre):
    contact(request)
    movies = Movie.objects.filter(genre = genre).order_by("id")
    paginator = Paginator(movies, 4)
    current_page = request.GET.get("page")
    movies = paginator.get_page(current_page)
    return render(request, "data/genre.html", {"genre" : genre, "movies" : movies})