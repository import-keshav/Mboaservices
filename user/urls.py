from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'user', api.UserViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for User
    path('user/user/', views.UserListView.as_view(), name='user_user_list'),
    path('user/user/create/', views.UserCreateView.as_view(), name='user_user_create'),
    path('user/user/detail/<slug:slug>/', views.UserDetailView.as_view(), name='user_user_detail'),
    path('user/user/update/<slug:slug>/', views.UserUpdateView.as_view(), name='user_user_update'),
)

