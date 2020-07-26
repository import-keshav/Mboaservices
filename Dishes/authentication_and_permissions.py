import jwt

from . import models

from Restaurant import models as restaurant_models

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import permissions


class CreateDishByRestaurantDataPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        restaurant = restaurant_models.Restaurant.objects.filter(pk=int(request.data['restaurant'])).first()
        return restaurant.owner.auth_token == access_token


class OperationOnDishByRestaurantDataPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        dish = models.Dish.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        return dish.restaurant.owner.auth_token == access_token


class CreateDishAddOnByRestaurantDataPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        dish = models.Dish.objects.filter(pk=int(request.data['dish'])).first()
        return dish.restaurant.owner.auth_token == access_token


class OperationOnDishAddOnByRestaurantDataPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        add_on = models.Dish.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        return add_on.dish.restaurant.owner.auth_token == access_token