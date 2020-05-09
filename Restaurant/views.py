from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status

from . import serializers as restaurant_serializers
from . import models as restaurant_models

from User import models as user_models

class CreateGetRestaurant(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return restaurant_serializers.RestaurantGetSerializer
        return restaurant_serializers.RestaurantPostSerializer


class UpdateRestaurant(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPostSerializer
    queryset = restaurant_models.Restaurant.objects.all()


class DeleteRestaurant(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPostSerializer
    queryset = restaurant_models.Restaurant.objects.all()


class CreateGetRestaurantEmployee(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        restaurant =  restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk']).first()
        return restaurant_models.RestaurantEmployee.objects.filter(restaurant=restaurant)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return restaurant_serializers.RestaurantEmployeeGetSerializer
        return restaurant_serializers.RestaurantEmployeePostSerializer


class DeleteRestaurantEmployee(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantEmployeePostSerializer
    queryset = restaurant_models.RestaurantEmployee.objects.all()

    def get_object(self):
        user = user_models.User.objects.filter(pk=self.request.data['user']).first()
        restaurant =  restaurant_models.Restaurant.objects.filter(pk=self.request.data['restaurant']).first()
        return restaurant_models.RestaurantEmployee.objects.filter(user=user, restaurant=restaurant)


class CreateGetRestaurantImage(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantImageSerializer

    def get_queryset(self):
        return restaurant_models.RestaurantImage.objects.filter(pk=self.kwargs['pk'])


class DeleteRestaurantImage(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantImageSerializer
    queryset = restaurant_models.RestaurantImage.objects.all()


class CreateGetRestaurantPromocode(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return restaurant_models.RestaurantPromocode.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return restaurant_serializers.RestaurantPromocodeGetSerializer
        return restaurant_serializers.RestaurantPromocodePostSerializer


class UpdateRestaurantPromocode(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPromocodePostSerializer
    queryset = restaurant_models.RestaurantPromocode.objects.all()


class DeleteRestaurantPromocode(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPromocodePostSerializer
    queryset = restaurant_models.RestaurantPromocode.objects.all()


class CreateGetRestaurantDriver(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return restaurant_models.RestaurantDriver.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return restaurant_serializers.RestaurantDriverGetSerializer
        return restaurant_serializers.RestaurantDriverPostSerializer


class UpdateRestaurantDriver(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantDriverPostSerializer
    queryset = restaurant_models.RestaurantDriver.objects.all()


class DeleteRestaurantDriver(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantDriverPostSerializer
    queryset = restaurant_models.RestaurantDriver.objects.all()
