from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MachineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.machine_id = self.scope['url_route']['kwargs']['pk']
        self.machine_group_name = 'machine_%s' % self.machine_id

        # Join machine group
        await self.channel_layer.group_add(
            self.machine_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.machine_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def machine_data(self, event):
        machine_data = event['machine_data']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'machine_data': machine_data
        }))


class MachineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.machine_group_name = 'machine_status_change'

        # Join machine group
        await self.channel_layer.group_add(
            self.machine_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.machine_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def machine_id_status(self, event):
        machine_id_status = event['machine_id_status']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'machine_id_status': machine_id_status
        }))
