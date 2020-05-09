import hashlib, binascii, os

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters

from . import models
from Client import models as client_models


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


class RegisterView(APIView):
    def post(self, request):
        try:
            data = self.request.data
            new_user_1 = models.User.objects.filter(email=data['email']).first()
            new_user_2 = models.User.objects.filter(mobile=data['mobile']).first()
            if not (new_user_1 and new_user_2):
                new_user = models.User(
                    name=data['name'],
                    email=data['email'],
                    mobile=data['mobile'],
                    avatar=data['avatar'],
                    password=hash_password(data['password'])
                )
                new_user.save()
                if data['which_user'] == 'client':
                    try:
                        user = models.User.objects.filter(mobile=data['mobile']).first()
                        new_user = client_models.Client(
                            user=user,
                            location_coordinates=data['location_coordinates'],
                            address=data['address'])
                        new_user.save()
                    except:
                        user = models.User.objects.filter(mobile=data['mobile']).first()
                        user.delete()
                        return Response({
                            "message": "(location_coordinates, address) any of params missing"
                        }, status=status.HTTP_400_BAD_REQUEST)
                elif data['which_user'] == 'restaurant_owner':
                    return Response(
                        {'message': 'Register Succesfully'},
                    status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "User with this credentials already exist!"
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "message": "(name, email, password, mobile, avatar, which_user, ) any of params missing"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'message': 'Register Succesfully', 'user_id': new_user.pk}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        try:
            data = self.request.data
            user = models.User.objects.filter(mobile=data['mobile']).first()
            if user:
                if verify_password(user.password, data['password']):
                    return Response(
                        {'message': 'Login Succesfully'}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                        {'message': 'User not exist with this mobile number'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                    {'message': '(mobile, password) any of params missing'}, status=status.HTTP_400_BAD_REQUEST)
