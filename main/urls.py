from django.urls import path
from .views import home, genre, about

urlpatterns = [
    path("", home, name="home"),
    path("genre/<str:genre>/", genre, name="genre" ),
    path("about/", about, name="about")
]
