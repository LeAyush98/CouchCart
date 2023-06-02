from django.urls import path
from .views import genre, search

urlpatterns = [
    path("genre/<str:genre>/", genre, name="genre" ),
    path("search/", search, name="search"),
]
