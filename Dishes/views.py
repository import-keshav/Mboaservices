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
    serializer_class = dish_serializers.DishUpdateSerializer
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


class DeleteDishImage(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishSerializer
    queryset = dish_models.DishImage.objects.all()


class IsAvailableOrNotDish(APIView):
    def post(self, request):
        if not 'dish' in self.request.data:
            return Response({"message": "Not Included dish if in data"}, status=status.HTTP_400_BAD_REQUEST)
        if not 'is_available' in self.request.data:
            return Response({"message": "not included is_available in data"}, status=status.HTTP_400_BAD_REQUEST)
        dish = dish_models.Dish.objects.filter(pk=self.request.data['dish']).first()
        dish.is_available = self.request.data['is_available']
        dish.save()
        return Response({"message": "Operation Done succesfully"}, status=status.HTTP_200_OK)