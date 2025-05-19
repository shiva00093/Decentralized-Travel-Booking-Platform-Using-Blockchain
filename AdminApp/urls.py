
from django.urls import path
from AdminApp import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('LogAction', views.LogAction),
    path('RegisterAction', views.RegisterAction),
    path('home', views.home),
    path('AddProducts', views.AddProducts),
    path('ProductAction', views.ProductAction),
    path('AddHotels', views.AddHotels),
    path('HotelAction', views.HotelAction),
    path('FlightAction', views.FlightAction),
    path('ViewAllRequests', views.ViewAllRequests),
    path('ViewProductsRequest', views.ViewProductsRequest),
    path('AcceptPRequest', views.AcceptPRequest),
    path('ViewHotelsRequest', views.ViewHotelsRequest),
    path('AcceptHRequest', views.AcceptHRequest),
    path('ViewFlightsRequests', views.ViewFlightsRequests),
    path('AcceptFRequest', views.AcceptFRequest),
]
