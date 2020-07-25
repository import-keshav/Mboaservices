import jwt

from . import models

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import permissions


class LogedInUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_heaader = request.headers.get('Authorization')
        if not authorization_heaader:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        client = models.Client.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        if client is None or client.user is None:
            raise exceptions.AuthenticationFailed('User not found')

        # self.enforce_csrf(request)
        return (client.user, None)


class ClientDataAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        client = models.Client.objects.filter(pk=int(request.META['PATH_INFO'].split('/')[-1])).first()
        return client.user == request.user