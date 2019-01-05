from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home, name='home'),
    path('vehicles/<slug>/', views.vehicle_list, name='vehicle_list'),
]