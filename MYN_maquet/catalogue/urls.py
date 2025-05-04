from django.urls import path
from . import views
urlpatterns = [
    path('',views.catalogue, name="catalogue"),
    path('panier/',views.panier, name="panier"),
    path('search/',views.search, name="search"),
]
