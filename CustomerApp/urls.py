
from django.urls import path
from CustomerApp import views

urlpatterns = [
    path('login', views.login),
    path('RegisterAction', views.RegisterAction),
    path('LogAction', views.LogAction),
    path('home', views.home),
    path('products', views.products),
    path('SearchAction', views.SearchAction),
    path('bookproduct', views.bookproduct),
    path('hotels', views.hotels),
    path('bookHotel', views.bookHotel),
    path('flights', views.flights),
    path('ViewFlightAction', views.ViewFlightAction),
    path('bookFlight', views.bookFlight),
    path('ViewBProducts', views.ViewBProducts),
    path('ViewBHotels', views.ViewBHotels),
    path('ViewBFlights', views.ViewBFlights),


]
