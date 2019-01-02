from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MachineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.machine_id = self.scope['url_route']['kwargs']['pk']
        self.machine_group_name = 'machine_%s' % self.machine_id

        # Join room group
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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        machine_data = text_data_json['machineData']

        # Send message to room group
        await self.channel_layer.group_send(
            self.machine_group_name,
            {
                'type': 'machineData',
                'machineData': machine_data
            }
        )

    # Receive message from room group
    async def machine_data_send(self, event):
        machine_data = event['machineData']
        print(machine_data)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'machineData': machine_data
        }))
