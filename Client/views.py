from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status

from . import serializers as client_serializers
from . import models as client_models

from User import models as user_models
from Restaurant import models as restaurant_models


class GetClient(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = client_models.Client.objects.all()
    serializer_class = client_serializers.ClientGetSerializer


class UpdateClient(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    queryset = client_models.Client.objects.all()
    serializer_class = client_serializers.ClientUpdateSerializer


class CreateGetClientNotification(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientNotificationSerializer

    def get_queryset(self):
        client = client_models.Client.objects.filter(pk=self.kwargs['pk']).first()
        return client_models.ClientNotification.objects.filter(client=client)


class CreateGetClientCart(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        client = client_models.Client.objects.filter(pk=self.kwargs['pk']).first()
        return client_models.ClientCart.objects.filter(client=client)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return client_serializers.ClientCartGetSerializer
        return client_serializers.ClientCartPostSerializer

    def create(self, request):
        client = client_models.Client.objects.filter(pk=self.request.data['client']).first()
        current_cart = client_models.ClientCart.objects.filter(client=client)
        new_restraurant = restaurant_models.Restaurant.objects.filter(pk=self.request.data['restaurant']).first()

        for item in current_cart:
            if item.restaurant != new_restraurant:
                client_models.ClientCart.objects.filter(client=client).delete()

        new_item = client_serializers.ClientCartPostSerializer(data=self.request.data)
        if new_item.is_valid():
            new_item.save()
            return Response({"message": "Item added Succesfully"}, status=status.HTTP_200_OK)
        return Response(new_item.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateClientCart(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientCartUpdateSerializer
    queryset = client_models.ClientCart.objects.all()


class DeleteClientCart(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientCartUpdateSerializer
    queryset = client_models.ClientCart.objects.all()


class CheckDishRestraurantInCart(APIView):
    def post(self, request):
        client = client_models.Client.objects.filter(pk=self.request.data['client']).first()
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.request.data['restaurant']).first()
        existence_restrau_dishes = client_models.ClientCart.objects.filter(client=client, restaurant=restaurant)
        current_client_cart = client_models.ClientCart.objects.filter(client=client)

        if current_client_cart  and existence_restrau_dishes:
            return Response({'is_restaurant_same': True}, status=status.HTTP_200_OK)
        return Response({'is_restaurant_same': False}, status=status.HTTP_200_OK)
