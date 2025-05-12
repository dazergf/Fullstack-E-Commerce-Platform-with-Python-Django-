from django.urls import path
from .views import register, login, mon_compte, accueil, home, reussi, logout,service_client,livraison

urlpatterns = [
    # path("", views.home, name="home"),
    path("register/", register, name="register"),
    path("connect/", login, name="login"),
    path("mon_compte/", mon_compte, name="mon_compte"),
    path("", accueil, name="accueil"),
    path("home/", home, name="home"),
    path("test/", reussi, name="reussi"),
    path('logout/', logout, name='logout'),path('livraison/', livraison, name='livraison'),
    path('service-client/', service_client, name='service_client'),
]