from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from . import serializers as driver_serializers
from . import models as driver_models


class GetDrivers(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = driver_serializers.DriverGetSerializer
    queryset = driver_models.Driver.objects.all()


class GetRestaurantDrivers(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = driver_serializers.DriverGetSerializer

    def get_queryset(self):
    	return [driver.driver for driver in driver_models.DriverRestaurant.objects.filter(restaurant__pk=self.kwargs['pk'])]
