from django.contrib import admin
from django.urls import path, include
from animals import views # Only if your HomeView is still in zoo_site/views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. The Homepage (handled by zoo_site views)
    path('', views.HomeView.as_view(), name='home'),
    
    # 2. Everything else (send to the animals app)
    path('animals/', include('animals.urls', namespace='animals')), 
]