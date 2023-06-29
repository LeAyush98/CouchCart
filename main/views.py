from django.shortcuts import render, redirect
from django.contrib import messages
from data.models import Movie, Cart
import smtplib
import boto3
import os
from dotenv import load_dotenv
from social_django.models import UserSocialAuth
from authApp.views import update_cart

load_dotenv(".env")


AWS_REGION = "ap-south-1"
ssm_client = boto3.client("ssm", region_name=AWS_REGION)

create_db = True

def mail(name:str, email:str, message:str) -> None:
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=EMAIL, password=PASSWORD)
    connection.sendmail(
        from_addr=email,
        to_addrs=EMAIL,
        msg=f"Subject:Hello!\n\n{message}\n\nThanks and regards,\n{name}"
    )
    connection.close()

def contact(request):
    if request.method == "POST":
        messages.success(request, "Message sent")
        mail(request.POST["name"], request.POST["email"], request.POST["message"])
        return redirect("home")

# Create your views here.
def home(request):
    contact(request)
    if request.user.is_authenticated:
        update_cart(request)
        items = Cart.objects.filter(user_id = request.user.id).count() 
    elif "items" in request.session:
        items = request.session["items"]
    else:
        items = 0    
    return render(request, "main/index.html", {"items" : items})


def about(request):
    contact(request)
    if request.user.is_authenticated:
        items = Cart.objects.filter(user_id = request.user.id).count() 
    elif "items" in request.session:
        items = request.session["items"]
    else:
        items = 0   
    return render(request, "main/about.html", {"items" : items})