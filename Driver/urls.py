from django.urls import path

from . import views

urlpatterns = [
	path('get-driver', views.GetDrivers.as_view()),
	path('get-restaurant-driver/<int:pk>', views.GetRestaurantDrivers.as_view()),
]