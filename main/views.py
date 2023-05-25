from django.shortcuts import render
from django.contrib import messages
import smtplib
from dotenv import load_dotenv
import os

load_dotenv(".env")

def mail(name:str, email:str, message:str) -> None:
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=EMAIL, password=PASSWORD)
    connection.sendmail(
        from_addr=email,
        to_addrs=EMAIL,
        msg=f"Subject:Hello!\n\n{message}\n\nThanks and regards,\n{name}"
    )
    connection.close()

# Create your views here.
def home(request):
    #messages.success(request, "Testing 123")
    if request.method == "POST":
        messages.success(request, "Message sent")
        mail(request.POST["name"], request.POST["email"], request.POST["message"])
    return render(request, "main/index.html", {})

def genre(request, genre):
    if request.method == "POST":
        messages.success(request, "Message sent")
        mail(request.POST["name"], request.POST["email"], request.POST["message"])

    return render(request, "main/generic.html", {"genre" : genre})

def about(request):
    return render(request, "main/about.html", {})