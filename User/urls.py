from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
	path('register', views.RegisterView.as_view()),
	path('login', views.LoginView.as_view()),
	path('change-password', views.ChangePassword.as_view()),
	path('restaurant-login', views.RestraurantLogin.as_view()),
	path('update-user/<int:pk>', views.UserUpdateProfile.as_view()),
	path('mobile-number-verification', views.MobileNumberVerification.as_view()),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
