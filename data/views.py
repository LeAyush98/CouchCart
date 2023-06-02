from django.shortcuts import render
from django.contrib import messages
from main.views import contact
from data.models import Movie, Cart
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .serialisers import MovieSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


# Create your views here.
def genre(request, genre):
    contact(request)
    movies = Movie.objects.filter(genre = genre).order_by("id")
    paginator = Paginator(movies, 4)
    current_page = request.GET.get("page")
    movies = paginator.get_page(current_page)
    return render(request, "data/genre.html", {"genre" : genre, "movies" : movies})

def search(request):
    if request.method == "POST":
        movie_name = request.POST["movie"]
        movies = Movie.objects.filter(name__icontains = movie_name).order_by("id")
        paginator = Paginator(movies, 4)
        current_page = request.GET.get("page")
        movies = paginator.get_page(current_page)
        return render(request, "data/genre.html", {"genre" : movie_name, "movies" : movies})
    return render(request, "data/search.html")
