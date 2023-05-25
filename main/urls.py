from django.urls import path
from .views import home, genre

urlpatterns = [
    path("", home, name="home"),
    path("genre/<str:genre>/", genre, name="genre" )
]
