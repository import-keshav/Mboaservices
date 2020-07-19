import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async

from . import models as invigilator_model
from Client import models as client_model

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        async_to_sync(self.save_message_in_database)(text_data_json)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_info': text_data_json
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        event = event['message_info']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'from': event['from']
        }))

    @database_sync_to_async
    def save_message_in_database(self, data):
        client =  async_to_sync(self.get_client)(data['client'])
        invigilator = async_to_sync(self.get_invigilator)(data['invigilator'])
        message_obj = invigilator_model.InvigilatorClientMessage(
            invigilator=invigilator,
            client=client,
            message=data['message'],
            message_from=data['from'])
        message_obj.save()

    @database_sync_to_async
    def get_client(self, client_id):
        return client_model.Client.objects.filter(pk=client_id).first()

    @database_sync_to_async
    def get_invigilator(self, invigilator_id):
        return invigilator_model.Invigilator.objects.filter(pk=invigilator_id).first()


class GetIncomingOrderForInvigilator(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['invigilator_id']
        self.room_group_name = 'incoming_order_for_invigilator_%s' % self.room_name

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

    def send_order_to_invigilator_group(self, event):
        self.send(text_data=json.dumps(event))