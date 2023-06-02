from django.shortcuts import render, redirect
from django.contrib import messages
from main.views import contact
from data.models import Movie, Cart
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .serialisers import MovieSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest

def make_cart_list(request: WSGIRequest) -> list:
    my_cart_list = []
    my_cart = Cart.objects.filter(user_id = request.user.id)
    for item in my_cart:
        my_cart_list.append(item.name)
    return my_cart_list    

# Create your views here.
def genre(request, genre):
    items = Cart.objects.filter(user_id = request.user.id).count()
    my_cart = make_cart_list(request)
    movies = Movie.objects.filter(genre = genre).order_by("id")
    paginator = Paginator(movies, 4)
    current_page = request.GET.get("page")
    movies = paginator.get_page(current_page)
    return render(request, "data/genre.html", {"genre" : genre, "movies" : movies, "items" : items, "my_cart" : my_cart})

def search(request):
    items = Cart.objects.filter(user_id = request.user.id).count()
    if request.method == "POST":
        movie_name = request.POST["movie"]
        movies = Movie.objects.filter(name__icontains = movie_name).order_by("id")
        paginator = Paginator(movies, 4)
        current_page = request.GET.get("page")
        movies = paginator.get_page(current_page)
        return render(request, "data/genre.html", {"genre" : movie_name, "movies" : movies, "items" : items})
    return render(request, "data/search.html", {"items" : items})

@login_required
def view_cart(request):
    items = Cart.objects.filter(user_id = request.user.id).count()
    items_in_cart = Cart.objects.filter(user_id = request.user.id)
    return render(request, "data/cart.html", {"items" : items, "items_in_cart" : items_in_cart})

@login_required
def add_to_cart(request, movie_id, user_id):
    if request.user.id == user_id:
        movie = Movie.objects.get(id = movie_id)
        buyer = User.objects.get(id = user_id)
        my_cart = make_cart_list(request)
        if movie.name not in my_cart:
            Cart.objects.create(
                name = movie.name,
                price = movie.price,
                user = buyer,
                movie = movie
            )
        items = Cart.objects.filter(user_id = request.user.id).count()
        
        movies = Movie.objects.filter(genre = movie.genre).order_by("id")
        paginator = Paginator(movies, 4)
        current_page = request.GET.get("page")
        movies = paginator.get_page(current_page)
        return render(request, "data/genre.html", {"genre" : movie.genre, "movies" : movies, "items" : items, "my_cart" : my_cart})
    else:
        messages.error(request, "You are not authorised to do that.")
        return redirect("home")
