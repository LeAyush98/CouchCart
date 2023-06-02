from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterUserForm
from data.models import Movie, Cart

# Create your views here.
def register_user(request):
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
            messages.success(request, f"Registration Successful! Welcome {str(username).title()}!")
            return redirect('home')
        else:
            messages.error(request, "There has been some error...")
            return redirect('register')
    else:
        form = RegisterUserForm()
        return render(request, "authApp/register.html", {"form" : form, "items" : items})

def login_user(request):
    items = Cart.objects.filter(user_id = request.user.id).count()
    if request.method == "POST":
        user = authenticate(request, username = request.POST["username"], password = request.POST["password"])
        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}!")
            return redirect("home")
        else:
            messages.success(request, f"Please check your credentials.")
            return redirect("login")
     
    return render(request, "authApp/login.html", {"items" : items})
    
def logout_user(request):
    logout(request) 
    messages.success(request , (f"Log Out Successful! Hope to see you again!"))   
    return redirect('home')    