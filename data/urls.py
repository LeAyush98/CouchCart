from django.urls import path
from .views import genre

urlpatterns = [
    path("genre/<str:genre>/", genre, name="genre" ),
]
