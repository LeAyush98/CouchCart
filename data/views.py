from django.shortcuts import render, redirect
from django.contrib import messages
from main.views import contact
from data.models import Movie, Cart
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .serialisers import MovieSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import Http404
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt   
import razorpay
import boto3
import os
from .forms import BillForm

AWS_REGION = "ap-south-1"
ssm_client = boto3.client("ssm", region_name=AWS_REGION)


def make_cart_list(request: WSGIRequest) -> list:
    my_cart_list = []
    my_cart = Cart.objects.filter(user_id = request.user.id)
    for item in my_cart:
        my_cart_list.append(item.name)
    return my_cart_list    

# To check if the url is typed directly instead of being redirected after payment
def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer

# Create your views here.
def genre(request, genre):
    if "movies_in_cart" not in request.session:
        request.session["movies_in_cart"] = []
    if "items" not in request.session:
        request.session["items"] = 0
    if request.user.is_authenticated:
        items = Cart.objects.filter(user_id = request.user.id).count() 
    elif "items" in request.session:
        items = request.session["items"]  
    my_cart = make_cart_list(request)
    movies = Movie.objects.filter(genre = genre).order_by("id")
    paginator = Paginator(movies, 4)
    current_page = request.GET.get("page")
    movies = paginator.get_page(current_page)
    return render(request, "data/genre.html", {"genre" : genre, "movies" : movies, "items" : items, "my_cart" : my_cart})

def search(request):
    if request.user.is_authenticated:
        items = Cart.objects.filter(user_id = request.user.id).count() 
    elif "items" in request.session:
        items = request.session["items"]
    if request.method == "POST":
        movie_name = request.POST["movie"]
        movies = Movie.objects.filter(name__icontains = movie_name).order_by("id")
        paginator = Paginator(movies, 4)
        current_page = request.GET.get("page")
        movies = paginator.get_page(current_page)
        return render(request, "data/genre.html", {"genre" : movie_name, "movies" : movies, "items" : items})
    return render(request, "data/search.html", {"items" : items})

def view_cart(request):
    if request.user.is_authenticated:
        items = Cart.objects.filter(user_id = request.user.id).count()
        items_in_cart = Cart.objects.filter(user_id = request.user.id)
        total_price = Cart.objects.filter(user_id = request.user.id).aggregate(Sum('price'))
        total_price = total_price['price__sum']
    else:
        items_in_cart = []
        total_price = 0
        items = request.session["items"] if "items" in request.session else 0    
        if "movies_in_cart" in request.session:
            for index, movie in enumerate(request.session["movies_in_cart"]):
                mov = Movie.objects.get(name = movie)
                items_in_cart.append(mov)
            for _ in items_in_cart:
                total_price+= _.price        

    return render(request, "data/cart.html", {"items" : items, "items_in_cart" : items_in_cart, "total_price" : total_price})


def add_to_cart(request, movie_id):
    movie = Movie.objects.get(id = movie_id)
    if movie not in request.session["movies_in_cart"]:
        request.session["items"] +=1
    
    if "movies_in_cart" not in request.session:
        request.session["movies_in_cart"] = []
    else:
        request.session["movies_in_cart"].append(movie.name)    
    
    if request.user.is_authenticated:
        try:
            Cart.objects.get(movie_id = movie_id)
        except:
            mov = Movie.objects.get(id = movie_id)
            Cart.objects.create(name = mov.name, price = mov.price, user = request.user, movie = mov)    
        items = Cart.objects.filter(user_id = request.user.id).count() 
    elif "items" in request.session:
        items = request.session["items"]
     
    my_cart = make_cart_list(request)
    movies = Movie.objects.filter(genre = movie.genre).order_by("id")
    paginator = Paginator(movies, 4)
    current_page = request.GET.get("page")
    movies = paginator.get_page(current_page)
    return render(request, "data/genre.html", {"genre" : movie.genre, "movies" : movies, "items" : items, "my_cart" : my_cart})


@login_required
def billing(request):
    items = Cart.objects.filter(user_id = request.user.id).count()
    items_in_cart = Cart.objects.filter(user_id = request.user.id)
    total_price = Cart.objects.filter(user_id = request.user.id).aggregate(Sum('price'))
    form = BillForm(initial= {"first_name" : request.user.first_name , "last_name" : request.user.last_name})
    try:
        amount = (int(total_price["price__sum"])*100)
    except TypeError:
        amount = 0
    KEY_ID = os.getenv("KEY_ID")
    KEY_SECRET = os.getenv("KEY_SECRET")
    if request.method == "POST":
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

    return render(request, "data/billing.html", {"items" : items, "items_in_cart" : items_in_cart, "total_price" : total_price['price__sum'], "KEY_ID" : KEY_ID, "amount" : amount, "form": form})
    

@csrf_exempt
@login_required
def success(request):
    items_in_cart = Cart.objects.filter(user_id = request.user.id)
    if not get_referer(request):
        raise Http404
    else:
        items_in_cart.delete() # As payment is success
    items = Cart.objects.filter(user_id = request.user.id).count() 
    return render(request, "data/success.html", {"items" : items})

@login_required
def delete_item(request, id):
    try:
        item_to_delete = Cart.objects.get(id=id)
        if request.user.id == item_to_delete.user_id:
            item_to_delete.delete()
            return redirect("view_cart")
        else:
            messages.error(request, "You are not authorised to do that.")
            return redirect("home")
    except ObjectDoesNotExist:
        return redirect("view_cart")
    