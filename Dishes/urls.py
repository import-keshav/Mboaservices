from django.urls import path

from . import views

urlpatterns = [
	path('get-homepage-dish', views.GetHomePageDishes.as_view()),

	path('create-dish', views.CreateGetDish.as_view()),
	path('get-specific-dish/<int:pk>', views.CreateGetDish.as_view()),
	path('get-dish-on-filter', views.GetDishOnFilter.as_view()),
	path('list-restaurant-dishes/<int:pk>', views.ListRestaurantDishes.as_view()),
	path('update-dish/<int:pk>', views.UpdateDish.as_view()),
	path('delete-dish/<int:pk>', views.DeleteDish.as_view()),
	path('is-available-or-not-dish/<int:pk>', views.IsAvailableOrNotDish.as_view()),

	path('get-dish-add-on/<int:pk>', views.GetDishAddOn.as_view()),
	path('add-dish-add-on', views.CreateDishAddOn.as_view()),
	path('update-dish-add-on/<int:pk>', views.UpdateDishAddOn.as_view()),
	path('delete-dish-add-on/<int:pk>', views.DeleteDishAddOn.as_view()),
]