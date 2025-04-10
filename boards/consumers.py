import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        self.room_group_name = f'board_{self.board_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'annotation_message',
                'data': data
            }
        )

    async def annotation_message(self, event):
        await self.send(text_data=json.dumps(event['data']))


    async def board_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
