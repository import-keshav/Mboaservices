from django.urls import path

from . import views

urlpatterns = [
	path('get-client/<int:pk>', views.GetClient.as_view()),
	path('update-client/<int:pk>', views.UpdateClient.as_view()),

	path('create-client-notification', views.CreateGetClientNotification.as_view()),
	path('get-client-notification/<int:pk>', views.CreateGetClientNotification.as_view()),

]