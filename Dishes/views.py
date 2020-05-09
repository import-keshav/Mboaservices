from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status

from . import serializers as dish_serializers
from . import models as dish_models

from Restaurant import models as restaurant_models


class CreateGetDish(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishSerializer

    def get_queryset(self):
        return dish_models.Dish.objects.filter(pk=self.kwargs['pk'])


class UpdateDish(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishSerializer
    queryset = dish_models.Dish.objects.all()


class DeleteDish(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishSerializer
    queryset = dish_models.Dish.objects.all()


class ListRestaurantDishes(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishSerializer

    def get_queryset(self):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk']).first()
        return dish_models.Dish.objects.filter(restaurant=restaurant)


class ListCreateDishImage(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishImageSerializer

    def get_queryset(self):
        dish = dish_models.Dish.objects.filter(pk=self.kwargs['pk']).first()
        return dish_models.DishImage.objects.filter(dish=dish)