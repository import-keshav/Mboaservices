import hashlib, binascii, os, random

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters

from . import models
from . import serializers as user_serializer
from Client import models as client_models
from Restaurant import models as restraurant_models
from Restaurant import serializers as restraurant_serializer

# from twilio.rest import Client

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


class ChangePassword(APIView):
    def post(self, request):
        try:
            user = models.User.objects.filter(mobile=self.request.data['mobile']).first()
            if not user:
                return Response({"message": "No user exists with this mobile number"})
            if verify_password(user.password, self.request.data['old_password']):
                user.password = hash_password(self.request.data['new_password'])
                user.save()
                return Response({"message": "Password changed Succesfully"})
            return Response({"message": "Invalid Old Password"})
        except:
            return Response({"message": "(mobile, old_password or new_password) is missing"})


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
                restrau_obj = restraurant_serializer.RestaurantGetSerializer(restraurant)
                return Response({'message': 'Login Succesfully', "restaurant": restrau_obj.data}, status=status.HTTP_200_OK)
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
            return Response({"message": 'User already Exists'})
        return Response({"message": "User didn't Exists"})


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

        account_sid = 'ACdb82fcbb9eabb02b0b3133cbab23943a '
        auth_token = '563eeb8eb2602ddba51516bb1a184f87'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=str(otp),
            from_='+12067373409',
            to='+919643906878'
        )
        return Response({"message": 'OTP Sent Succesfully'})


class VerifyOTP(APIView):
    def post(self, request):
        for key in ['mobile_number', 'otp']:
            if not key in self.request.data:
                return Response(
                    {"message": "(mobile_number, otp) any of params missing"},
                    status=status.HTTP_400_BAD_REQUEST)
        mobile_number = self.request.data['mobile_number']
        otp = self.request.data['otp']

        obj = models.MobileNumberOTP.objects.filter(mobile=mobile_number).first()
        if not obj:
            return Response({
                "message": "Mobile Number is not Verified"
            }, status=status.HTTP_400_BAD_REQUEST)

        if obj.otp == otp:
            obj.delete()
            return Response({"message": "Mobile Numbered Verified"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)




# from authy.api import AuthyApiClient
# authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)
# authy_api.phones.verification_start(
#     mobile_number,
#     self.request.data['country_code'],
#     via="sms"
# )
