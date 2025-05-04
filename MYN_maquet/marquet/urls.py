from django.urls import path
from .views import register, login, mon_compte, acceuil, home, reussi

urlpatterns = [
    # path("", views.home, name="home"),
    path("index/", register, name="registere"),
    path("connect/", login, name="login"),
    path("home/mon_compte/", mon_compte, name="mon_compte"),
    path("", acceuil, name="acceuil"),
    path("home/", home, name="home"),
    path("test/", reussi, name="reussi"),
]