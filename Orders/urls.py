from django.urls import path

from . import views

urlpatterns = [
	path('create-order', views.CreateOrder.as_view()),
	path('update-order/<int:pk>', views.UpdateOrder.as_view()),
	path('update-order-status', views.UpdateOrderStatus.as_view()),

	path('get-client-past-orders/<int:pk>', views.GetClientPastOrders.as_view()),
	path('get-restaurant-past-orders/<int:pk>', views.GetRestaurantPastOrders.as_view()),
]