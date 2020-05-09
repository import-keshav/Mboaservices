from django.urls import path

from . import views

urlpatterns = [
	path('create-dish', views.CreateGetDish.as_view()),
	path('get-specific-dish/<int:pk>', views.CreateGetDish.as_view()),
	path('list-restaurant-dishes/<int:pk>', views.ListRestaurantDishes.as_view()),
	path('update-dish/<int:pk>', views.UpdateDish.as_view()),
	path('delete-dish/<int:pk>', views.DeleteDish.as_view()),

	path('create-dish-image', views.ListCreateDishImage.as_view()),
	path('get-dish-images/<int:pk>', views.ListCreateDishImage.as_view()),
	path('delete-dish-image/<int:pk>', views.DeleteDishImage.as_view()),

]