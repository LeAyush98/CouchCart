from django.contrib import admin
from .models import Movie, Cart
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    model = Movie
    fields = ["name","year","genre","price","duration","rating","synopsis","image"]

class CartAdmin(admin.ModelAdmin):
    model = Cart
    fields = ["name","price","user"]

admin.site.register(Movie, MovieAdmin)
admin.site.register(Cart, CartAdmin)    