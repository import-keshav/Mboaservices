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

    def create_order_data(self, incoming_order):
        order_dishes = models.OrderDish.objects.filter(order=incoming_order.order)
        dishes = [serializers.GetOrderDishSerializer(dish).data for dish in order_dishes]
        return json.dumps({
            'order': serializers.GetOrderSerializer(incoming_order.order).data,
            'dishes': dishes,
        })

    def get_incoming_orders(self, restaurant_id, last_id):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=restaurant_id).first()
        return models.IncomingOrder.objects.filter(restaurant=restaurant, pk__gte=last_id)

    def send_and_get_messages(self, restaurant_id):
        new_data = self.get_incoming_orders(restaurant_id, 0)
        last_id = new_data[len(new_data)-1].pk
        while self.is_opened:
            for incoming_order in new_data:
                order_data = self.create_order_data(incoming_order)
                async_to_sync(self.send)({
                    "type": "websocket.send",
                    "text": order_data 
                })
            new_data = self.get_incoming_orders(restaurant_id, last_id+1)
            if len(new_data) >0:
                last_id = new_data[len(new_data)-1].pk 
            time.sleep(60)

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
            time.sleep(60)

    @database_sync_to_async
    def get_order_status(self, order_id):
        return models.Order.objects.filter(pk=int(order_id)).first().status

    async def websocket_disconnect(self, event):
        self.is_opened = False
        await self.send({
            'type': 'websocket.disconnect'
        })
