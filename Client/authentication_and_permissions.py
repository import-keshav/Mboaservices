import jwt

from . import models

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import permissions


class ClientDataAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        client = models.Client.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        return client.user.auth_token == access_token


class ClientCartPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return False
        access_token = authorization_header.split(' ')[1]
        if 'client' in request.data:
            client = models.Client.objects.filter(pk=int(request.data['client'])).first()
            return client.user.auth_token == access_token
        else:
            cart = models.ClientCart.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
            return cart.client.user.auth_token == access_token
