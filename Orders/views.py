import pika

from django import forms
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters

from . import serializers as orders_serializers
from . import models as orders_models

from Restaurant import models as restaurant_models
from Dishes import models as dish_models
from Client import models as client_models

class CreateOrder(APIView):
    def post(self, request):
        if 'order' not in self.request.data:
            return Response({'message': 'Include Order in Data'})
        if 'dishes' not in self.request.data:
            return Response({'message': 'Include Dish in Data'})

        order_serializer = orders_serializers.CreateOrderSerializer(data=self.request.data['order'])
        if order_serializer.is_valid():
            self.validate_dishes(self.request.data['dishes'], self.request.data['order']['restaurant'])
            order_serializer.save()
            self.add_order_in_restaurant_queue(self.request.data['order']['restaurant'], order_serializer.data['id'])
            self.create_order(self.request.data['dishes'], order_serializer.data['id'])
            return Response({'message': 'Orders Created Successfully', 'id': order_serializer.data['id']})
        return Response(order_serializer.errors)


    def validate_dishes(self, dishes, restaurant):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=restaurant).first()
        if not restaurant:
            raise forms.ValidationError("Invalid Restaurant ID")
        for dish in dishes:
            order_dish_serializer = orders_serializers.CreateOrderDisheSerializer(data=dish)
            if not order_dish_serializer.is_valid():
                raise forms.ValidationError(order_dish_serializer.errors)
            if not dish_models.Dish.objects.filter(restaurant=restaurant, pk=dish['dish']).first():
                raise forms.ValidationError("Dish Id not matched with Restaurant Id")


    def create_order(self, dishes, order):
        for dish in dishes:
            dish['order'] = order
            order_dish_serializer = orders_serializers.CreateOrderDisheSerializer(data=dish)
            if order_dish_serializer.is_valid():
                order_dish_serializer.save()                


    def add_order_in_restaurant_queue(self, restaurant, order):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=restaurant).first()
        order = orders_models.Order.objects.filter(pk=order).first()
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue=restaurant.unique_id + '_recieve_order')
        channel.basic_publish(
            exchange='',
            routing_key=restaurant.unique_id + '_recieve_order',
            body=str(order.id)
        )
        connection.close()


class UpdateOrder(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.UpdateOrderSerializer
    queryset = orders_models.Order.objects.all()


class UpdateOrderStatus(APIView):
    def post(self, request):
        valid_keys = ['status', 'order']
        for key in valid_keys:
            if not key in self.request.data:
                raise forms.ValidationError(key + " is missing")

        status = self.request.data['status']
        order = orders_models.Order.objects.filter(pk=self.request.data['order']).first()
        self.update_order_status(status, order)
        return Response({'message': 'Order Updates Successfully'})

    def update_order_status(self, status, order):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue=order.restaurant.unique_id + '_order_staus')
        channel.basic_publish(
            exchange='',
            routing_key=order.restaurant.unique_id + '_order_staus',
            body=str({'order': order.pk, 'status': status})
        )
        connection.close()
        order.status = status
        order.save()



class GetClientPastOrders(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.GetClientRestaurantPastOrdersSerializer

    def get_queryset(self):
        client = client_models.Client.objects.filter(pk=self.kwargs['pk']).first()
        return orders_models.Order.objects.filter(client=client)


class GetRestaurantPastOrders(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.GetClientRestaurantPastOrdersSerializer

    def get_queryset(self):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk']).first()
        return orders_models.Order.objects.filter(restaurant=restaurant)