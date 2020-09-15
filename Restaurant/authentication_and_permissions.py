import jwt

from . import models

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import permissions


class RestaurantDataPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        restaurant = models.Restaurant.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        return restaurant.auth_token == access_token


class CreateOperationsOnRestaurantPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        restaurant = models.Restaurant.objects.filter(pk=int(request.data["restaurant"])).first()
        return restaurant.auth_token == access_token


class RestaurantPromocodeDataPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        promocode = models.RestaurantPromocode.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        return promocode.restaurant.auth_token == access_token
