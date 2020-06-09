from django.urls import path

from . import views

urlpatterns = [
	path('create-client-review', views.CreateGetClientReview.as_view()),
	path('get-client-review/<int:pk>', views.CreateGetClientReview.as_view()),
	path('get-restaurant-review/<int:pk>', views.GetRestaurantReview.as_view()),	
]