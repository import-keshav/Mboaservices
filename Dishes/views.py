from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters

from . import serializers as dish_serializers
from . import models as dish_models
from . import authentication_and_permissions

from Restaurant import models as restaurant_models


class GetHomePageDishes(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = dish_models.GeneralDish.objects.all()
    serializer_class = dish_serializers.GeneralDishGetSerializer


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
    permission_classes = [authentication_and_permissions.OperationOnDishByRestaurantDataPermission]


class DeleteDish(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishUpdateSerializer
    queryset = dish_models.Dish.objects.all()
    permission_classes = [authentication_and_permissions.OperationOnDishByRestaurantDataPermission]


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
    permission_classes = [authentication_and_permissions.OperationOnDishByRestaurantDataPermission]
    def post(self, request, pk):
        if not 'is_available' in self.request.data:
            return Response({"message": "not included is_available in data"}, status=status.HTTP_400_BAD_REQUEST)
        dish = dish_models.Dish.objects.filter(pk=pk).first()
        if not dish:
            return Response({"message": "Invalid Dish ID"}, status=status.HTTP_400_BAD_REQUEST)
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


class GetDishAddOn(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishAddOnsGetSerializer

    def get_queryset(self):
        dish = dish_models.Dish.objects.filter(pk=self.kwargs['pk']).first()
        return dish_models.DishAddOns.objects.filter(dish=dish)


class CreateDishAddOn(generics.CreateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishAddOnsPostSerializer
    permission_classes = [authentication_and_permissions.CreateDishAddOnByRestaurantDataPermission]


class DeleteDishAddOn(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishAddOnsGetSerializer
    queryset = dish_models.DishAddOns.objects.all()
    permission_classes = [authentication_and_permissions.OperationOnDishAddOnByRestaurantDataPermission]


class UpdateDishAddOn(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = dish_serializers.DishAddOnsGetSerializer
    queryset = dish_models.DishAddOns.objects.all()
    permission_classes = [authentication_and_permissions.OperationOnDishAddOnByRestaurantDataPermission]
