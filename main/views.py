from django.shortcuts import render, redirect
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

def contact(request):
    if request.method == "POST":
        messages.success(request, "Message sent")
        mail(request.POST["name"], request.POST["email"], request.POST["message"])
        return redirect("home")

# Create your views here.
def home(request):
    contact(request)
    return render(request, "main/index.html", {})


def about(request):
    contact(request)
    return render(request, "main/about.html", {})