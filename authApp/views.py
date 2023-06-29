from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterUserForm
from data.models import Movie, Cart

def update_cart(request):
    if "movies_in_cart" in request.session:
        for index, movie in enumerate(request.session["movies_in_cart"]):
            mov = Movie.objects.get(name = movie)
            try:
                in_cart = Cart.objects.get(name=mov.name)
            except:    
                Cart.objects.create(name = movie, price = mov.price, user = request.user, movie = mov)

# Create your views here.
def register_user(request):
    if "items" in request.session:
        items = request.session["items"] 
    else:
        items = Cart.objects.filter(user_id = request.user.id).count()    
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = authenticate(request, username=username, password=password, email = email, first_name = first_name, last_name = last_name)
            login(request, user)
            update_cart(request)
            messages.success(request, f"Registration Successful! Welcome {str(username).title()}!")
            return redirect('home')
        else:
            messages.error(request, "There has been some error...")
            return redirect('register')
    else:
        form = RegisterUserForm()
        return render(request, "authApp/register.html", {"form" : form, "items" : items})

def login_user(request):
    if "items" in request.session:
        items = request.session["items"] 
    else:
        items = Cart.objects.filter(user_id = request.user.id).count()    
    if request.method == "POST":
        user = authenticate(request, username = request.POST["username"], password = request.POST["password"])
        if user:
            login(request, user)
            update_cart(request)
            messages.success(request, f"Welcome {user.first_name}!")
            return redirect("home")
        else:
            messages.success(request, f"Please check your credentials.")
            return redirect("login")
     
    return render(request, "authApp/login.html", {"items" : items})
    
def logout_user(request):
    update_cart(request)
    logout(request) 
    messages.success(request , (f"Log Out Successful! Hope to see you again!"))   
    return redirect('home')    