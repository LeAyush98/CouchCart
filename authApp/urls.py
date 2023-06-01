from django.urls import path, include
from .views import login_user, register_user, logout_user

urlpatterns = [
    path("accounts/", include('allauth.urls')),
    path("login/", login_user, name= "login"),
    path("register/", register_user, name= "register"),
    path("logout/", logout_user, name= "logout"),
]
