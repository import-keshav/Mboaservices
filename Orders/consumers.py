import asyncio
import json
import pika
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from threading import Thread

from . import models
from . import serializers
from Restaurant import models as restaurant_models

from asgiref.sync import async_to_sync


class IncomingRestaurantOrders(AsyncConsumer):
    async def websocket_connect(self, data):
        await self.send({
            "type": "websocket.accept",
        })
        self.is_opened = True
        restaurant_unique_id = await self.get_restaurant_unique_id(self.scope['url_route']['kwargs']['pk'])
        channel = self._connect(restaurant_unique_id)
        t1 = Thread(target=self.send_and_get_messages, args=(channel, restaurant_unique_id))
        t1.start()


    def _connect(self, restaurant_unique_id):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=restaurant_unique_id + '_recieve_order')
        channel.exchange_declare(exchange='recieve_order',
            exchange_type='fanout')
        channel.queue_bind(exchange='recieve_order',
            queue=restaurant_unique_id + '_recieve_order')
        return channel

    @database_sync_to_async
    def create_order_data(self, order_id):
        order = models.Order.objects.filter(pk=int(order_id)).first()
        order_dishes = models.OrderDish.objects.filter(order=order)
        dishes = [serializers.GetOrderDishSerializer(dish).data for dish in order_dishes]
        return json.dumps({
            'order': serializers.GetOrderSerializer(order).data,
            'dishes': dishes,
        })

    @database_sync_to_async
    def get_restaurant_unique_id(self, pk):
        return restaurant_models.Restaurant.objects.filter(pk=pk)[0].unique_id

    def send_and_get_messages(self, channel, restaurant_unique_id):
        while self.is_opened:
            for (method_frame, _, body) in channel.consume(restaurant_unique_id + '_recieve_order'):
                order_data = async_to_sync(self.create_order_data)(body.decode('ascii'))
                async_to_sync(self.send)({
                    "type": "websocket.send",
                    "text": order_data
                })

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
        restaurant_unique_id = await self.get_restaurant_unique_id(order_id)
        channel = self._connect(restaurant_unique_id)
        self.is_opened = True
        t1 = Thread(target=self.send_and_get_messages, args=(channel, restaurant_unique_id, order_id))
        t1.start()


    def send_and_get_messages(self, channel, restaurant_unique_id, order_id):
        while self.is_opened:
            for (method_frame, _, body) in channel.consume(restaurant_unique_id + '_order_status'):
                incoming_order_data = eval(body.decode('ascii'))
                if int(incoming_order_data["order"]) == int(order_id):
                    incoming_order_data = json.dumps(incoming_order_data)
                    async_to_sync(self.send)({
                        "type": "websocket.send",
                        "text": incoming_order_data,
                    })

    def _connect(self, restaurant_unique_id):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue=restaurant_unique_id + '_order_status')
        channel.exchange_declare(exchange='order_status',
                         exchange_type='fanout')
        channel.queue_bind(exchange='order_status',
            queue=restaurant_unique_id + '_order_status')
        return channel

    @database_sync_to_async
    def get_restaurant_unique_id(self, order_id):
        return models.Order.objects.filter(pk=int(order_id)).first().restaurant.unique_id

    async def websocket_disconnect(self, event):
        self.is_opened = False
        await self.send({
            'type': 'websocket.disconnect'
        })
