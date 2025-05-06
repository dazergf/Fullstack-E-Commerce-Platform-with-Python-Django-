from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', include("marquet.urls")),
    path('admin/', lambda request: redirect('http://localhost/phpmyadmin')),
    path('catalogue/', include("catalogue.urls")),
    
]
