from django.urls import path

from . import views

urlpatterns = [
	path('create-restaurant', views.CreateGetRestaurant.as_view()),
	path('get-restaurant-on-home-page', views.GetAllRestaurant.as_view()),
	path('get-restaurant/<int:pk>', views.CreateGetRestaurant.as_view()),
	path('get-restaurant-on-filter', views.GetRestaurantOnFilter.as_view()),
	path('update-restaurant/<int:pk>', views.UpdateRestaurant.as_view()),
	path('delete-restaurant/<int:pk>', views.DeleteRestaurant.as_view()),
	path('open-close-restaurant', views.OpenCloseRestaurant.as_view()),

	path('create-restaurant-employee', views.CreateGetRestaurantEmployee.as_view()),
	path('get-restaurant-employee/<int:pk>', views.CreateGetRestaurantEmployee.as_view()),
	path('delete-restaurant-employee', views.DeleteRestaurantEmployee.as_view()),

	path('create-promocode', views.CreateGetRestaurantPromocode.as_view()),
	path('get-promocode/<int:pk>', views.CreateGetRestaurantPromocode.as_view()),
	path('update-promocode/<int:pk>', views.UpdateRestaurantPromocode.as_view()),
	path('delete-promocode/<int:pk>', views.DeleteRestaurantPromocode.as_view()),

	path('create-restaurant-driver', views.CreateGetRestaurantDriver.as_view()),
	path('get-restaurant-driver/<int:pk>', views.CreateGetRestaurantDriver.as_view()),
	path('update-restaurant-driver/<int:pk>', views.UpdateRestaurantDriver.as_view()),
	path('delete-restaurant-driver/<int:pk>', views.DeleteRestaurantDriver.as_view()),
	path('get-restaurant-specific-driver/<int:pk>', views.GetRestaurantSpecifiDriver.as_view()),

]
