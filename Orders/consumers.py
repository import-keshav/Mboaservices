import asyncio
import json
import pika
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from . import models
from . import serializers
from Restaurant import models as restaurant_models


class IncomingRestaurantOrders(AsyncConsumer):
    async def websocket_connect(self, data):
        await self.send({
            "type": "websocket.accept",
        })

        restaurant_unique_id = await self.get_restaurant_unique_id(self.scope['url_route']['kwargs']['pk'])
        channel = self._connect(restaurant_unique_id)

        while 1:
            for (method_frame, _, body) in channel.consume(restaurant_unique_id + '_recieve_order'):
                order_data = await self.create_order_data(body.decode('ascii'))
                await self.send({
                    "type": "websocket.send",
                    "text": order_data,
                })


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
        dishes = []
        for dish in order_dishes:
            dishes.append(serializers.GetOrderDishSerializer(dish).data) 

        return json.dumps({
            'order': serializers.GetOrderSerializer(order).data,
            'dishes': dishes,
        })


    @database_sync_to_async
    def get_restaurant_unique_id(self, pk):
        return restaurant_models.Restaurant.objects.filter(pk=pk)[0].unique_id

    # def websocket_receive(self, data):
    #     pass

    async def websocket_disconnect(self, event):
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

        while 1:
            for (method_frame, _, body) in channel.consume(restaurant_unique_id + '_order_status'):
                incoming_order_data = eval(body.decode('ascii'))
                if int(incoming_order_data["order"]) == int(order_id):
                    incoming_order_data = json.dumps(incoming_order_data)
                    print(incoming_order_data)
                    await self.send({
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
        await self.send({
            'type': 'websocket.disconnect'
        })