import hashlib
import binascii
import os
import random
import jwt

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters

from twilio.rest import Client

from . import models
from . import serializers as user_serializer
from Client import models as client_models
from Client import serializers as client_serializers
from Restaurant import models as restraurant_models
from Restaurant import serializers as restraurant_serializer
from Invigilator import models as invigilator_models
from Invigilator import serializers as invigilator_serializer

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def create_jwt(user_obj):
    """Function for creating JWT for Authentication Purpose"""
    return jwt.encode(user_serializer.UserSerializer(user_obj).data, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


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
            import pdb;pdb.set_trace()
            data = self.request.data
            new_user = models.User.objects.filter(mobile=data['mobile']).first()
            if not new_user:
                user = models.User(
                    name=data['name'],
                    mobile=data['mobile'],
                )
                user.save()
                user = models.User.objects.filter(mobile=data['mobile']).first()
                client_user = client_models.Client(user=user)
                client_user.save()
            else:
                return Response({
                    "message": "User with this credentials already exist!"
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "message": "(name, mobile,) any of params missing"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'message': 'Register Succesfully', 'user_id': client_user.pk}, status=status.HTTP_200_OK)


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


class ChangeRestaurantPassword(APIView):
    def post(self, request):
        try:
            restaurant = restraurant_models.Restaurant.objects.filter(pk=self.request.data['restaurant_id']).first()
            if not restaurant:
                return Response({"message": "No Restaurant exists with this id"})
            if verify_password(restaurant.owner.password, self.request.data['old_password']):
                restaurant.owner.password = self.request.data['new_password']
                restaurant.owner.save()
                restaurant.save()
                return Response({"message": "Password changed Succesfully"})
            return Response({"message": "Invalid Old Password"})
        except:
            return Response({"message": "(restaurant_id, old_password or new_password) is missing"})


class UserUpdateProfile(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    queryset = models.User.objects.all()
    serializer_class = user_serializer.UserSerializer


class RestraurantLogin(APIView):
    def post(self, request):
        try:
            restraurant = restraurant_models.Restaurant.objects.filter(
                unique_id=self.request.data['restraurant_unique_id']).first()
            if not restraurant:
                return Response({"message": "Invalid Restraurant unique Id",}, status=status.HTTP_400_BAD_REQUEST)
            if verify_password( restraurant.owner.password, self.request.data['password']):
                restraurant.owner.auth_token = ""
                restraurant.owner.password = self.request.data['password']
                restraurant.owner.save()
                restrau_obj = restraurant_serializer.RestaurantGetSerializer(restraurant)
                jwt_token = create_jwt(restrau_obj.data)
                restraurant.owner.auth_token = jwt_token
                restraurant.owner.save()
                restraurant.owner.password = self.request.data['password']
                restraurant.owner.save()
                return Response({'message': 'Login Succesfully', "restaurant": restrau_obj.data, "token":jwt_token}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "restraurant_unique_id is missing"}, status=status.HTTP_400_BAD_REQUEST)


class CheckMobileNumber(APIView):
    def post(self, request):
        if not 'mobile_number' in self.request.data:
            return Response({
                "message": "Mobile Number Missing"
            }, status=status.HTTP_400_BAD_REQUEST)
        mobile_number = self.request.data['mobile_number']

        obj = models.User.objects.filter(mobile=mobile_number).first()
        if obj:
            return Response({
                "message": 'User already Exists',
                'is_valid' : True},
                status=status.HTTP_200_OK)
        return Response({
            "message": "User didn't Exists",
            'is_valid' : False},
            status=status.HTTP_200_OK)


class SendOTP(APIView):
    def post(self, request):
        if not 'mobile_number' in self.request.data:
            return Response({
                "message": "Mobile Number Missing"
            }, status=status.HTTP_400_BAD_REQUEST)

        mobile_number = self.request.data['mobile_number']
        otp = random.randrange(1000,9999)
        obj = models.MobileNumberOTP.objects.filter(mobile=mobile_number).first()
        if obj:
            obj.otp = otp
        else:
            obj = models.MobileNumberOTP(mobile=mobile_number, otp=otp)
        obj.save()

        # account_sid = 'ACdb82fcbb9eabb02b0b3133cbab23943a'
        # auth_token = '3897c742069ec3c7da110a73b1af17ee'
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body=str(otp),
        #     from_='+12067373409',
        #     to=mobile_number
        # )
        return Response({
            "message": 'OTP Sent Succesfully',
            'otp': str(otp)},
            status=status.HTTP_200_OK)


class GetAuthToken(APIView):
    def post(self, request):
        if not 'mobile_number' in self.request.data:
            return Response(
                {"message": "Mobile Number is missing"},
                status=status.HTTP_400_BAD_REQUEST)
        mobile_number = self.request.data['mobile_number']

        user = models.User.objects.filter(mobile=mobile_number).first()
        if not user:
            return Response({
                "message": "No User exist with this Mobile Number"
            }, status=status.HTTP_400_BAD_REQUEST)
        user.auth_token = ""
        user.save()
        jwt_token = create_jwt(user)
        user.auth_token = jwt_token
        user.save()
        client = client_models.Client.objects.filter(user=user).first()
        if not client:
            return Response({"message": "Invalid Client"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "token":jwt_token,
            "client": client_serializers.ClientGetSerializer(client).data
            }, status=status.HTTP_200_OK)


class InvigilatorLogin(APIView):
    def post(self, request):
        try:
            invigilator = invigilator_models.Invigilator.objects.filter(user__mobile=self.request.data['mobile_number']).first()
            if not invigilator:
                return Response({"message": "No User Exist with this Mobile Number",}, status=status.HTTP_400_BAD_REQUEST)
            if verify_password(invigilator.user.password, self.request.data['password']):
                invigilator.user.auth_token = ""
                invigilator.user.password = self.request.data['password']
                invigilator.user.save()
                invigilator.save()

                invigilator_obj = invigilator_serializer.InvigilatorGetSerializer(invigilator)
                jwt_token = create_jwt(invigilator_obj.data)
                invigilator.user.auth_token = jwt_token
                invigilator.user.password = self.request.data['password']
                invigilator.user.save()
                invigilator.save()
                return Response({'message': 'Login Succesfully', "invigilator": invigilator_obj.data, "token":jwt_token}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "restraurant_unique_id is missing"}, status=status.HTTP_400_BAD_REQUEST)

class ChangeInvigilatorPassword(APIView):
    def post(self, request):
        try:
            invigilator = invigilator_models.Invigilator.objects.filter(pk=self.request.data['pk']).first()
            if not invigilator:
                return Response({"message": "No User Exist with this Mobile Number",}, status=status.HTTP_400_BAD_REQUEST)
            if verify_password(invigilator.user.password, self.request.data['old_password']):
                invigilator.user.password = self.request.data['new_password']
                invigilator.user.save()
                invigilator.save()
                return Response({"message": "Password changed Succesfully"})
            return Response({"message": "Invalid Old Password"})
        except:
            return Response({"message": "(mobile_number, old_password or new_password) is missing"})

{"name": "Keshav", "mobile": "+919643906878"}