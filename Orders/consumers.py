import asyncio
import json
import time
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from threading import Thread

from . import models
from . import serializers
from Restaurant import models as restaurant_models


class IncomingRestaurantOrders(AsyncConsumer):
    async def websocket_connect(self, data):
        await self.send({
            "type": "websocket.accept",
        })
        self.is_opened = True
        restaurant_id = self.scope['url_route']['kwargs']['pk']
        t1 = Thread(target=self.send_and_get_messages, args=(restaurant_id,))
        t1.start()

    @database_sync_to_async
    def create_order_data(self, incoming_order):
        order_dishes = models.OrderDish.objects.filter(order=incoming_order.order)
        dishes = [serializers.GetOrderDishSerializer(dish).data for dish in order_dishes]
        return json.dumps({
            'order': serializers.GetOrderSerializer(incoming_order.order).data,
            'dishes': dishes,
        })

    @database_sync_to_async
    def get_incoming_orders(self, restaurant_id):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=restaurant_id).first()
        return models.IncomingOrder.objects.filter(restaurant=restaurant)

    def send_and_get_messages(self, restaurant_id):
        while self.is_opened:
            incoming_orders = async_to_sync(self.get_incoming_orders)(restaurant_id)
            for incoming_order in incoming_orders:
                order_data = async_to_sync(self.create_order_data)(incoming_order)
                async_to_sync(self.send)({
                    "type": "websocket.send",
                    "text": order_data 
                })
            time.sleep(120)

    async def websocket_disconnect(self, event):
        self.is_opened = False
        await self.send({
            'type': 'websocket.disconnect'
        })


class GetOrderStatus(AsyncConsumer):
    async def websocket_connect(self, data):
        await self.send({
            "type": "websocket.accept",
        })
        order_id = self.scope['url_route']['kwargs']['pk']
        self.is_opened = True
        t1 = Thread(target=self.send_and_get_messages, args=(order_id,))
        t1.start()


    def send_and_get_messages(self, order_id):
        while self.is_opened:
            async_to_sync(self.send)({
                "type": "websocket.send",
                "text": async_to_sync(self.get_order_status)(order_id),
            })
            time.sleep(120)

    @database_sync_to_async
    def get_order_status(self, order_id):
        return models.Order.objects.filter(pk=int(order_id)).first().status

    async def websocket_disconnect(self, event):
        self.is_opened = False
        await self.send({
            'type': 'websocket.disconnect'
        })
