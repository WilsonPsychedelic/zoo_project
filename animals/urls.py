from django.urls import path
from . import views # This looks for views inside the ANIMALS folder
from .views import SignUpView

app_name = 'animals'

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('', views.HomeView.as_view(), name='home'),
    path('list/', views.AnimalListView.as_view(), name='animal-list'), 
    path('add/', views.AnimalCreateView.as_view(), name='animal-create'),
    path('search/', views.AnimalSearchView.as_view(), name='animal-search'),
    path('<int:pk>/edit/', views.AnimalUpdateView.as_view(), name='animal-update'),
    path('<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal-delete'),
    path('archive/', views.AnimalArchiveIndexView.as_view(), name='animal-archive-index'),
    path('today/', views.AnimalTodayArchiveView.as_view(), name='animal-today-archive'),
]