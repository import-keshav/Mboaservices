from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status, filters

from . import serializers as restaurant_serializers
from . import models as restaurant_models
from . import authentication_and_permissions

from User import models as user_models
from Reviews import models as review_models

class CreateGetRestaurant(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return restaurant_serializers.RestaurantGetSerializer
        return restaurant_serializers.RestaurantPostSerializer


class GetAllRestaurantPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class GetAllRestaurant(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantGetSerializer
    queryset = restaurant_models.Restaurant.objects.all().order_by('-rating')
    pagination_class = GetAllRestaurantPagination


class GetRestaurantOnFilter(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    queryset = restaurant_models.Restaurant.objects.all()
    serializer_class = restaurant_serializers.RestaurantGetSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category__name', 'name']
    search_fields = ['category__name', 'name']


class UpdateRestaurant(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantUpdateSerializer
    queryset = restaurant_models.Restaurant.objects.all()
    permission_classes = [authentication_and_permissions.RestaurantDataPermission]


class DeleteRestaurant(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPostSerializer
    queryset = restaurant_models.Restaurant.objects.all()
    permission_classes = [authentication_and_permissions.RestaurantDataPermission]


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


class GetRestaurantPromocode(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPromocodeGetSerializer

    def get_queryset(self):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk']).first()
        return restaurant_models.RestaurantPromocode.objects.filter(restaurant=restaurant)


class CreateRestaurantPromocode(generics.CreateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPromocodePostSerializer
    permission_classes = [authentication_and_permissions.CreateOperationsOnRestaurantPermission]


class UpdateRestaurantPromocode(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPromocodeUpdateSerializer
    queryset = restaurant_models.RestaurantPromocode.objects.all()
    permission_classes = [authentication_and_permissions.RestaurantDataPermission]


class DeleteRestaurantPromocode(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantPromocodePostSerializer
    queryset = restaurant_models.RestaurantPromocode.objects.all()
    permission_classes = [authentication_and_permissions.RestaurantDataPermission]


class CreateGetRestaurantDriver(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk']).first()
        return restaurant_models.RestaurantDriver.objects.filter(restaurant=restaurant)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return restaurant_serializers.RestaurantDriverGetSerializer
        return restaurant_serializers.RestaurantDriverPostSerializer


class UpdateRestaurantDriver(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantDriverUpdateSerializer
    queryset = restaurant_models.RestaurantDriver.objects.all()
    permission_classes = [authentication_and_permissions.RestaurantDataPermission]


class DeleteRestaurantDriver(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantDriverPostSerializer
    queryset = restaurant_models.RestaurantDriver.objects.all()
    permission_classes = [authentication_and_permissions.RestaurantDataPermission]


class GetRestaurantSpecifiDriver(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = restaurant_serializers.RestaurantDriverGetSerializer

    def get_queryset(self):
        return restaurant_models.RestaurantDriver.objects.filter(pk=self.kwargs['pk'])


class OpenCloseRestaurant(APIView):
    permission_classes = [authentication_and_permissions.RestaurantDataPermission]
    def post(self, request, pk):
        if not 'is_open' in self.request.data:
            return Response({"message": "not included is_open in data"}, status=status.HTTP_400_BAD_REQUEST)
        restaurant = restaurant_models.Restaurant.objects.filter(pk=pk).first()
        restaurant.is_open = self.request.data['is_open']
        restaurant.save()
        return Response({"message": "Operation Done succesfully"}, status=status.HTTP_200_OK)
