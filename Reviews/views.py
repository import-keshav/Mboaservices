from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters

from . import serializers as review_serializers
from . import models as review_models

from Client import models as client_models
from Restaurant import models as restaurant_models


class CreateGetClientReview(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        client = client_models.Client.objects.filter(pk=self.kwargs['pk']).first()
        return review_models.ClientReview.objects.filter(client=client)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return review_serializers.GetClientReviewSerializer
        return review_serializers.PostClientReviewSerializer


class GetRestaurantReview(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = review_serializers.GetClientReviewSerializer

    def get_queryset(self):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk']).first()
        return review_models.ClientReview.objects.filter(restaurant=restaurant)
