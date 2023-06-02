from django.urls import path
from .views import genre, search, view_cart, add_to_cart

urlpatterns = [
    path("genre/<str:genre>/", genre, name="genre" ),
    path("search/", search, name="search"),
    path("cart/", view_cart, name="view_cart"),
    path("add/<int:user_id>/<int:movie_id>/", add_to_cart, name="add_to_cart")
]
