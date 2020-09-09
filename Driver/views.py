from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from . import serializers as driver_serializers
from . import models as driver_models


class GetRestaurantDriver(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = driver_serializers.DriverGetSerializer
    queryset = driver_models.Driver.objects.all()
