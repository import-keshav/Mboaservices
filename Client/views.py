from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status

from . import serializers as client_serializers
from . import models as client_models
from . import authentication_and_permissions

from User import models as user_models
from Restaurant import models as restaurant_models


class GetClient(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientGetSerializer
    permission_classes = [authentication_and_permissions.ClientDataAccessPermission]
    def get_queryset(self):
        return client_models.Client.objects.filter(pk=self.kwargs['pk'])


class UpdateClient(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    queryset = client_models.Client.objects.all()
    serializer_class = client_serializers.ClientUpdateSerializer
    permission_classes = [authentication_and_permissions.ClientDataAccessPermission]


class CreateGetClientNotification(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientNotificationSerializer
    permission_classes = [authentication_and_permissions.ClientDataAccessPermission]

    def get_queryset(self):
        client = client_models.Client.objects.filter(pk=self.kwargs['pk']).first()
        return client_models.ClientNotification.objects.filter(client=client)


class CreateGetClientCart(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [authentication_and_permissions.ClientDataAccessPermission]

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
            return Response(new_item.data, status=status.HTTP_200_OK)
        return Response(new_item.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateClientCart(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientCartUpdateSerializer
    queryset = client_models.ClientCart.objects.all()
    permission_classes = [authentication_and_permissions.ClientDataAccessPermission]


class DeleteClientCart(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientCartUpdateSerializer
    queryset = client_models.ClientCart.objects.all()
    permission_classes = [authentication_and_permissions.ClientDataAccessPermission]


class CheckDishRestraurantInCart(APIView):
    permission_classes = [authentication_and_permissions.ClientDataAccessPermission]

    def post(self, request):
        client = client_models.Client.objects.filter(pk=self.request.data['client']).first()
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.request.data['restaurant']).first()
        existence_restrau_dishes = client_models.ClientCart.objects.filter(client=client, restaurant=restaurant)
        current_client_cart = client_models.ClientCart.objects.filter(client=client)

        if current_client_cart  and existence_restrau_dishes:
            return Response({'is_restaurant_same': True}, status=status.HTTP_200_OK)
        return Response({'is_restaurant_same': False}, status=status.HTTP_200_OK)


class GetPriceOfCartItem(APIView):
    permission_classes = [authentication_and_permissions.ClientDataAccessPermission]
    
    def get(self, request, pk):
        cart_item =  client_models.ClientCart.objects.filter(pk=pk).first()
        price = cart_item.dish.price * cart_item.num_of_items
        for add_on in cart_item.add_ons.all():
            if not add_on.is_free:
                price += (add_on.price * cart_item.num_of_items)
        cart_item.price = price
        cart_item.save()
        return Response({'price': price}, status=status.HTTP_200_OK)