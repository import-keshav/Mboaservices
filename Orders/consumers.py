import asyncio
import json
import time
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

from . import models
from . import serializers
from Orders import serializers as orders_serializers
from Orders import models as orders_models
from Restaurant import models as restaurant_models


class IncomingRestaurantOrders(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'restaurant_incoming_order_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("Channel Disconnected Successfully")

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_incoming_order_to_restaurant',
                'order_id': text_data_json['order_id']
            }
        )

    def send_incoming_order_to_restaurant(self, event):
        order_data = self.create_order_data(event['order_id'])
        self.send(text_data=json.dumps(order_data))

    def create_order_data(self, order_id):
        order = async_to_sync(self.get_order_from_order_id)(order_id)
        order_dishes = models.OrderDish.objects.filter(order=order)
        dishes = [serializers.GetOrderDishSerializer(dish).data for dish in order_dishes]
        return {
            'order': serializers.GetOrderSerializer(order).data,
            'dishes': dishes,
        }

    @database_sync_to_async
    def get_order_from_order_id(self, order_id):
        return orders_models.Order.objects.filter(pk=order_id).first()


class UpdateGetOrderStatus(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'restaurant_order_status_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("Channel Disconnected Successfully")

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_order_status',
                'order_status_info': text_data_json
            }
        )

    # Receive message from room group
    def send_order_status(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'order_status_info': event['order_status_info'],
        }))
