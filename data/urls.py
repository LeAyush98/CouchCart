from django.urls import path
from .views import genre, search, view_cart, add_to_cart, success, delete_item, billing

urlpatterns = [
    path("genre/<str:genre>/", genre, name="genre" ),
    path("search/", search, name="search"),
    path("cart/", view_cart, name="view_cart"),
    path("add/<int:movie_id>/", add_to_cart, name="add_to_cart"),
    path("success/", success, name="success"),
    path("delete/<int:id>", delete_item, name="delete_item"),
    path("billing/", billing, name="billing")
]
