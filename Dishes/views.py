from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters

from . import serializers as dish_serializers
from . import models as dish_models

from Restaurant import models as restaurant_models


class CreateGetDish(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return dish_models.Dish.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return dish_serializers.DishGetSerializer
        return dish_serializers.DishPostSerializer


class UpdateDish(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishUpdateSerializer
    queryset = dish_models.Dish.objects.all()


class DeleteDish(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishUpdateSerializer
    queryset = dish_models.Dish.objects.all()


class ListRestaurantDishes(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    def list(self, request, pk):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=pk).first()
        dishes = dish_models.Dish.objects.filter(restaurant=restaurant)
        data = {}
        for dish in dishes:
            categories = dish.categories.all()
            for category in categories:
                dish_serializer_obj = dish_serializers.DishGetSerializer(dish)
                if category.name in data:
                    data[category.name].append(dish_serializer_obj.data)
                else:
                    data[category.name] = [dish_serializer_obj.data]
        return Response(data, status=status.HTTP_200_OK)


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


class GetDishOnFilter(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = dish_models.Dish.objects.all()
    serializer_class = dish_serializers.DishGetSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['categories__name', 'name']
    search_fields = ['categories__name', 'name']


class AddGetDishAddOn(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        dish = dish_models.Dish.objects.filter(pk=self.kwargs['pk']).first()
        return dish_models.DishAddOns.objects.filter(dish=dish)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return dish_serializers.DishAddOnsGetSerializer
        return dish_serializers.DishAddOnsPostSerializer


class DeleteDishAddOn(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishAddOnsGetSerializer
    queryset = dish_models.DishAddOns.objects.all()


class UpdateDishAddOn(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishAddOnsGetSerializer
    queryset = dish_models.DishAddOns.objects.all()