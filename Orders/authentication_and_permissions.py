import jwt

from . import models
from Client import models as client_models

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import permissions


class CreateOrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        client = client_models.Client.objects.filter(pk=int(request.data['order']['client'])).first()
        return client.user.auth_token == access_token


class UpdateDeleteOrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        order = models.Order.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        return order.restaurant.auth_token == access_token


class RestaurantOperationsOnOrders(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        order = models.Order.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        return order.restaurant.auth_token == access_token
