from django.urls import path

from . import views

urlpatterns = [
	path('get-driver', views.GetRestaurantDriver.as_view()),
]