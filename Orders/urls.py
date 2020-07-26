from django.urls import path

from . import views

urlpatterns = [
	path('create-order', views.CreateOrder.as_view()),
	path('update-order/<int:pk>', views.UpdateOrder.as_view()),
	path('accept-order/<int:pk>', views.AcceptOrder.as_view()),
	path('reject-order/<int:pk>', views.RejectOrder.as_view()),
	path('order-completed', views.OrderCompleted.as_view()),

	path('get-incoming-orders/<int:pk>', views.GetIncomingOrders.as_view()),
	path('get-ongoing-orders/<int:pk>', views.GetOngoingOrders.as_view()),
	path('get-specific-order/<int:pk>', views.GetSpecificOrder.as_view()),
	path('get-client-past-orders/<int:pk>', views.GetClientPastOrders.as_view()),
	path('get-restaurant-past-orders/<int:pk>', views.GetRestaurantPastOrders.as_view()),
]