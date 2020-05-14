from django.urls import path

from . import views

urlpatterns = [
	path('get-client/<int:pk>', views.GetClient.as_view()),
	path('update-client/<int:pk>', views.UpdateClient.as_view()),

	path('create-client-notification', views.CreateGetClientNotification.as_view()),
	path('get-client-notification/<int:pk>', views.CreateGetClientNotification.as_view()),

	path('get-client-cart/<int:pk>', views.CreateGetClientCart.as_view()),
	path('add-item-in-client-cart', views.CreateGetClientCart.as_view()),
	path('update-item-in-client-cart/<int:pk>', views.UpdateClientCart.as_view()),
	path('delete-item-in-client-cart/<int:pk>', views.DeleteClientCart.as_view()),

]