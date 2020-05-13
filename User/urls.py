from django.urls import path

from . import views

urlpatterns = [
	path('register', views.RegisterView.as_view()),
	path('login', views.LoginView.as_view()),
	path('change-password', views.ChangePassword.as_view()),
	path('restaurant-login', views.RestraurantLogin.as_view()),
	path('update-user/<int:pk>', views.UserUpdateProfile.as_view()),
]
