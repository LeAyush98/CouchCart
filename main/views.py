from django.shortcuts import render, redirect
from django.contrib import messages
from data.models import Movie, Cart
import smtplib
import boto3
import os
from data.db_maker import add_data

AWS_REGION = "ap-south-1"
ssm_client = boto3.client("ssm", region_name=AWS_REGION)

create_db = True

def mail(name:str, email:str, message:str) -> None:
    EMAIL = ssm_client.get_parameter(Name='contact_email', WithDecryption=True)['Parameter']['Value']
    PASSWORD = ssm_client.get_parameter(Name='contact_password', WithDecryption=True)['Parameter']['Value']

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
    items = Cart.objects.filter(user_id = request.user.id).count()
    return render(request, "main/index.html", {"items" : items})


def about(request):
    global create_db
    if create_db:
        add_data()
        create_db = False
    contact(request)
    items = Cart.objects.filter(user_id = request.user.id).count()
    return render(request, "main/about.html", {"items" : items})