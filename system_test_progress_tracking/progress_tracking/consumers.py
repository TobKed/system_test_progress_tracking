from channels.generic.websocket import WebsocketConsumer
import json


class MachineConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        machine_data = text_data_json['machineData']

        self.send(text_data=json.dumps({
            'machineData': machine_data
        }))
